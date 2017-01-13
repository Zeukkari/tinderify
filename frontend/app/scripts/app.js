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
  .config(function ($routeProvider) {
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
      }).when('/chat/:id', {
        templateUrl: 'views/chat.html',
        controller: 'ChatCtrl',
        controllerAs: 'chat'
      })
      .otherwise({
        redirectTo: '/'
      });
//      $locationProvider.hashPrefix('');
  })
  .factory("Users", function($resource) {
    return $resource("http://localhost:5000/api/users")
  }).factory("Matches", function($resource) {
    return $resource("http://localhost:5000/api/matches")
  }).factory("Messages", function($resource) {
    return $resource("http://localhost:5000/api/message")
  }).factory("Statistics", function($resource) {
    return $resource("http://localhost:5000/api/statistics")
  })
  ;