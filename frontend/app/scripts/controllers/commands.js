'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the tinderApp
 */
angular.module('tinderApp')
  .controller('CommandsCtrl', ['$scope', 'Autolike', function ($scope, Autolike) {

    this.autolike = function() {
     Autolike.get();
     };
 }]);
