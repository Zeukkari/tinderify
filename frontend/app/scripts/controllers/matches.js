'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the tinderApp
 */
angular.module('tinderApp')
  .controller('MatchCtrl', ['$scope', 'Matches', 'Users', 'Messages', 'Updates', '$interval', function ($scope, Matches, Users, Messages, Updates, $interval) {

   this.matches = Matches.get();
   this.openChat = function(id) {
    this.isChatEnabled = true;
    this.currentId = id;
    this.messages = sortMessages(this.matches[id].messages);
   }

   this.sendMessage = () => Messages.save({"id" : this.currentId, "body" : this.chatMessage});

   this.getUpdates = function() {
        Updates.get(function(updates) {
            for (match of updates) {
                var existingMatch = this.matches[update[id]];
                // TODO: handle new matches
                if (existingMatch === undefined) {
                    continue;
                }
                existingMatch.messages = sortMessages(_.unionBy(existingMatch.messages, match, "id"));
            }
   });


  };
         $interval(this.getUpdates, 10000);
  }]);

function sortMessages(messages) {
    return _.sortBy(messages, (message) => Date.parse(message.sent)).reverse();
}