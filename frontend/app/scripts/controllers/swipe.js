'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description Controller for the main page
 */
angular.module('tinderApp')
    .controller('SwipeCtrl', ['$scope', 'Recommendations', function($scope, Recommendations) {
        this.recommendations = Recommendations.get();
    }]);
