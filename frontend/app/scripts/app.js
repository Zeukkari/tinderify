'use strict';

/**
 * @ngdoc overview
 * @name tinderApp
 * @description
 * # tinderApp
 *
 * Main module of the application.
 */
angular
    .module('tinderApp', [
        'ngResource',
        'ngRoute'
    ])
    .config(function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'MainCtrl',
                controllerAs: 'main'
            })
            .when('/matches', {
                templateUrl: 'views/matches.html',
                controller: 'MatchCtrl',
                controllerAs: 'match'
            }).when('/commands', {
                templateUrl: 'views/commands.html',
                controller: 'CommandsCtrl',
                controllerAs: 'commands'
            })
            .otherwise({
                redirectTo: '/'
            });
        //      $locationProvider.hashPrefix('');
    }).factory("Users", function($resource) {
        return $resource("http://localhost:5000/api/users")
    }).factory("Matches", function($resource) {
        return $resource("http://localhost:5000/api/matches")
    }).factory("Messages", function($resource) {
        return $resource("http://localhost:5000/api/message")
    }).factory("Statistics", function($resource) {
        return $resource("http://localhost:5000/api/statistics")
    }).factory("Updates", function($resource) {
        return $resource("http://localhost:5000/api/updates")
    }).factory("Autolike", function($resource) {
        return $resource("http://localhost:5000/api/autolike")
    });
