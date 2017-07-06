'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:MainCtrl
 * @description Controller for the main page
 */
angular.module('tinderApp')
  .controller('SwipeCtrl', ['$scope', 'Recommendations', 'JudgeRecommendation', function($scope, Recommendations, JudgeRecommendation) {

    this.loadNewRecommendations = () => {

      Recommendations.get((data) => {
        this.currentIndex = 0;
        this.recommendations = data;
        this.currentRecommendation = this.recommendations[0];
      });
    };

    this.init = () => {
      this.loadNewRecommendations();
    };

    this.init();

    this.judge = (like) => {
      JudgeRecommendation.save({
        "id": this.currentRecommendation.id,
        "like": like
      });
      if (this.currentIndex + 1 == this.recommendations.length) {
        this.loadNewRecommendations();
      } else {
        this.currentRecommendation = this.recommendations[++this.currentIndex];
      }
    }
  }]);
