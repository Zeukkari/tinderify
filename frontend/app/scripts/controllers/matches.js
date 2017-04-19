'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MatchCtrl
 * @description controller for the matches page
 */
angular.module('tinderApp')
    .controller('MatchCtrl', ['$scope', 'Matches', 'Users', 'Messages', 'Updates', '$interval', 'ngDialog',
        function($scope, Matches, Users, Messages, Updates, $interval, ngDialog) {

            this.lastSuccesfulUpdate = ""; // Contains last succesful made update as an ISO date string
            this.isMatchListEnabled = true;

            Matches.get((data) => {
                this.matches = data.toJSON();
                this.sortedKeys = this.sortMatchKeys(this.matches);
            });

            // Open chat with the given user
            this.openChat = (id) => {
                this.isChatEnabled = true;
                this.isMatchListEnabled = false;
                this.currentId = id;
                this.messages = this.sortMessages(this.matches[id].messages);
                this.currentMatch = this.matches[id];
                // $("#matchphotos").slick();
            }

            this.sortMessages = (messages) => {
                return _.sortBy(messages, (message) => {
                    return message.sent;
                }).reverse();
            };

            this.sortMatchKeys = (matches) => {
                return _.sortBy(matches, (match) => {
                    return match.messages.length == 0 ? 0 : match.messages[match.messages.length - 1].sent
                }).reverse().map((element) => {return element.id});
            };

            this.returnFromChat = () => {
              this.isChatEnabled = false;
              this.isMatchListEnabled = true;
            }

            this.openPhotos = id => {
                ngDialog.open({
                    template: "views/photos.html",
                    data: this.matches[id],
                    width: "80%"
                });
            }

            // Send message to a given user
            this.sendMessage = () => Messages.save({
                "id": this.currentId,
                "body": this.chatMessage
            });

            // Get updates, like new matches, new messages, removed users, profile changes
            this.getUpdates = () => {
                Updates.get({
                    since: this.lastSuccesfulUpdate
                }, (data) => {
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
                        existingMatch.messages = this.sortMessages(_.unionBy(existingMatch.messages, updatedMatch.messages, "id"));
                    }
                });
                this.sortedKeys = this.sortMatchKeys(this.matches);
                this.lastSuccesfulUpdate = new Date().toISOString();
            };
            $interval(this.getUpdates, 10000); // Periodically get new updates
        }
    ]);
