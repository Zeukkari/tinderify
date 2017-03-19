'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MatchCtrl
 * @description controller for the matches page
 */
angular.module('tinderApp')
    .controller('MatchCtrl', ['$scope', 'Matches', 'Users', 'Messages', 'Updates', '$interval', function($scope, Matches, Users, Messages, Updates, $interval) {

        this.matches = Matches.get();
        this.openChat = function(id) {
            this.isChatEnabled = true;
            this.currentId = id;
            this.messages = sortMessages(this.matches[id].messages);
        }

        this.sendMessage = () => Messages.save({
            "id": this.currentId,
            "body": this.chatMessage
        });

        // Get updates, like new matches, new messages, removed users, profile changes
        this.getUpdates = () => {
            Updates.get((updates) => {
                for (match of updates) {
                    let existingMatch = this.matches[update[id]];
                    // TODO: handle new matches
                    if (existingMatch === undefined) {
                        continue;
                    }
                    existingMatch.messages = sortMessages(_.unionBy(existingMatch.messages, match, "id"));
                }
            });
        };
        $interval(this.getUpdates, 10000); // Periodically get new updates
    }]);

function sortMessages(messages) {
    return _.sortBy(messages, (message) => Date.parse(message.sent)).reverse();
}
