'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MatchCtrl
 * @description controller for the matches page
 */
angular.module('tinderApp')
  .controller('MatchCtrl', ['$scope', 'Matches', 'MatchMessage', '$interval', '$timeout', 'ngDialog', 'mySocket',
    function($scope, Matches, MatchMessage, $interval, $timeout, ngDialog, mySocket) {

      this.init = () => {
        this.lastSuccesfulUpdate = ""; // Contains last succesful made update as an ISO date string
        this.isMatchListEnabled = true;
        this.activeSlideIndex = 0;
        this.matches = {};
        this.getUpdates();
      }

      // Open chat with the given user
      this.openChat = (id) => {
        this.isChatEnabled = true;
        this.isMatchListEnabled = false;
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
          return match.last_activity_date
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
          width: "80%",
          height: 700,
          controller: ['$scope', function($scope) {
            $scope.active = 0;
          }]
        });
      }

      // Send message to a given user
      this.sendMessage = () => MatchMessage.save({
        "id": this.currentMatch.match_id,
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
          console.info("current = " + this.currentMatch);

          // Also remember to update the current match whose chat is active
          if (this.currentMatch !== undefined && this.currentMatch.id === existingMatch.id) {
            this.currentMatch = existingMatch;
          }
        }

        this.sortedKeys = this.sortMatchKeys(this.matches);
        this.lastSuccesfulUpdate = new Date().toISOString();

        // $timeout(this.getUpdates, 10000);

      };

      var processUpdates = this.processUpdates;
      mySocket.on('updates', function(updates) {
        console.log("received updates");
        processUpdates(updates);
      });

      this.init();

    }
  ]);
