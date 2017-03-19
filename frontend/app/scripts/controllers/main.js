'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description Controller for the main page
 */
angular.module('tinderApp')
    .controller('MainCtrl', ['$scope', 'Users', 'Statistics', function ($scope, Users, Statistics) {

        this.statistics = Statistics.get();
    }]);
