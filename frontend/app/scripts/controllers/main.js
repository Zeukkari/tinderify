'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description Controller for the main page
 */
angular.module('tinderApp')
    .controller('MainCtrl', ['$scope', 'Statistics', function($scope, Statistics) {
        this.statistics = Statistics.get();

    }]);
