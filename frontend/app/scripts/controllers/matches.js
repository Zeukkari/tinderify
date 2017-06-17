'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MatchCtrl
 * @description controller for the matches page
 */
angular.module('tinderApp')
    .controller('MatchCtrl', ['$scope', 'Matches', 'MatchMessage', '$interval', '$timeout', 'ngDialog', 'mySocket',
        function($scope, Matches, Messages, $interval, $timeout, ngDialog, mySocket) {

            mySocket.on('updates', function() {
                console.log("received updates");
            });

            this.init = () => {
                this.lastSuccesfulUpdate = ""; // Contains last succesful made update as an ISO date string
                this.isMatchListEnabled = true;
                this.matches = {};
                this.getUpdates();
            }

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
                });
            };

            this.sortMatchKeys = (matches) => {
                return _.sortBy(matches, (match) => {
                    return match.messages.length == 0 ? 0 : match.messages[match.messages.length - 1].sent
                }).reverse().map((element) => {
                    return element.id
                });
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
            this.sendMessage = () => MatchMessage.save({
                "id": this.currentId,
                "body": this.chatMessage
            });

            // Get updates, like new matches, new messages, removed users, profile changes
            this.getUpdates = () => {
                Matches.get({
                    since: this.lastSuccesfulUpdate
                }, (data) => {
                    this.processUpdates(data.toJSON())
                });
            };

            this.processUpdates = (updates) => {
                // let updates = data.toJSON()
                for (let id in updates) {
                    let existingMatch = this.matches[id];
                    let updatedMatch = updates[id];

                    console.info(existingMatch);
                    console.info(updatedMatch);

                    // If there is no existing match a new user has been matched
                    // Let's add this to the list of matches
                    if (existingMatch === undefined) {
                        this.matches[id] = updatedMatch;
                        continue;
                    }
                    // Update any new received messages

                    existingMatch.messages = this.sortMessages(_.unionBy(existingMatch.messages, updatedMatch.messages, "id"));
                    console.info(existingMatch);
                }

                this.sortedKeys = this.sortMatchKeys(this.matches);
                this.lastSuccesfulUpdate = new Date().toISOString();

                $timeout(this.getUpdates, 10000);

            };

            this.init();

        }
    ]);
