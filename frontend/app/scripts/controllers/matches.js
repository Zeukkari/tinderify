'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MatchCtrl
 * @description controller for the matches page
 */
angular.module('tinderApp')
    .controller('MatchCtrl', ['$scope', 'Matches', 'Users', 'Messages', 'Updates', '$interval', function($scope, Matches, Users, Messages, Updates, $interval) {
        this.matches = Matches.get();

        // Open chat with the given user
        this.openChat = function(id) {
            this.isChatEnabled = true;
            this.currentId = id;
            this.messages = sortMessages(this.matches[id].messages);
        }

        // Send message to a given user
        this.sendMessage = () => Messages.save({
            "id": this.currentId,
            "body": this.chatMessage
        });

        var lastSuccesfulUpdate = ""; // Contains last succesful made update as an ISO date string

        // Get updates, like new matches, new messages, removed users, profile changes
        this.getUpdates = () => {
            Updates.get({since : lastSuccesfulUpdate}, (data) => {
                let updates = data.toJSON()
                for (let id in updates) {
                    let existingMatch = this.matches[id];
                    let updatedMatch = updates[id];
                    // If there is no existing match a new user has been matched
                    // Let's add this to the list of matches
                    if (existingMatch === undefined) {
                        this.matches[id] = updatedMatch;
                        continue;
                    }
                    // Update any new received messages
                    console.log(existingMatch);
                    console.log(updatedMatch);
                    existingMatch.messages = sortMessages(_.unionBy(existingMatch.messages, updatedMatch.messages, "id"));
                }
            });
            lastSuccesfulUpdate = new Date().toISOString();
        };
        $interval(this.getUpdates, 10000); // Periodically get new updates
    }]);

function sortMessages(messages) {
    return _.sortBy(messages, (message) => Date.parse(message.sent)).reverse();
}
