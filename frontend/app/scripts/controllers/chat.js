'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the tinderApp
 */
angular.module('tinderApp')
  .controller('ChatCtrl', ['$scope', 'Matches', function ($scope, Matches) {

//  this.matches = "foobar";

   this.matches = Matches.get(function(data) {
//      $('.slides').slick();
//      $scope.matches = data;
   });

  }]);
