'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the tinderApp
 */
angular.module('tinderApp')
  .controller('MainCtrl', ['$scope', 'Users', 'Statistics', function ($scope, Users, Statistics) {

    this.statistics = Statistics.get();
}]);
