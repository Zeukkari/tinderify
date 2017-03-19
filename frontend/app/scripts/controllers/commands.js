'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:CommandsCtrl
 * @description controller for the commands page
 */
angular.module('tinderApp')
    .controller('CommandsCtrl', ['$scope', 'Autolike', function ($scope, Autolike) {

        this.autolike = () => Autolike.get();
    }]);
