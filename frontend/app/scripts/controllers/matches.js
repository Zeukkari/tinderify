'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the tinderApp
 */
angular.module('tinderApp')
  .controller('MatchCtrl', ['$scope', 'Matches', 'Users', 'Messages', function ($scope, Matches, Users, Messages) {

   this.matches = Matches.get();

   this.openChat = function(id) {
    this.isChatEnabled = true;
    this.currentId = id;
    this.messages = this.matches[id].messages;
   }

   this.sendMessage = () => Messages.save({"id" : this.currentId, "body" : this.chatMessage});

  }]);
