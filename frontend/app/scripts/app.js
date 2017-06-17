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
        'ngRoute', 'ngDialog', 'btford.socket-io'
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
            }).when('/photos', {
              templateUrl: 'view/photos.html'
            })
            .otherwise({
                redirectTo: '/'
            });
        //      $locationProvider.hashPrefix('');
    }).factory("Matches", function($resource) {
        return $resource("http://localhost:5000/api/matches")
    }).factory("MatchMessage", function($resource) {
        return $resource("http://localhost:5000/api/matches/:id/message")
    }).factory("Statistics", function($resource) {
        return $resource("http://localhost:5000/api/commands/statistics")
    }).factory("Autolike", function($resource) {
        return $resource("http://localhost:5000/api/commands/autolike")
    }).factory('mySocket', function (socketFactory) {
  return socketFactory();
});
