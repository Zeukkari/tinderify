'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:SwipeCtrl
 * @description Controller for the swiping page
 */
angular.module('tinderApp')
  .controller('SwipeCtrl', ['$scope', 'Recommendations', 'JudgeRecommendation', '$window', '$interval', '$timeout', function($scope, Recommendations, JudgeRecommendation, $window, $interval, $timeout) {

    this.loadNewRecommendations = () => {
      this.isLoading = true;
      this.loadingInterval = $interval(() => {
        this.loadingText = this.loadingText.length == 3 ? "" : this.loadingText + "."
      }, 300);

      Recommendations.get((data) => {
        $interval.cancel(this.loadingInterval);
        this.isLoading = false;
        this.currentIndex = 0;
        this.recommendations = data;
        this.currentRecommendation = this.recommendations[0];
      });
    };

    this.init = () => {
      this.loadingText = "";
      this.isLoading = false;
      this.loadNewRecommendations();
      this.showMatchInfo = false;
    };

    this.init();

    this.showMatchedNotification = () => {
      this.showMatchInfo = true;
      $timeout(() => {
        this.showMatchInfo = false
      }, 100);
    };

    this.judge = (like) => {
      JudgeRecommendation.save({
        "id": this.currentRecommendation.id,
        "like": like
      }, (data) => {
        if (data.matched) {
          this.showMatchedNotification();
        }
      });
      if (this.currentIndex + 1 == this.recommendations.length) {
        this.loadNewRecommendations();
      } else {
        this.currentRecommendation = this.recommendations[++this.currentIndex];
      }
    };

    var judgeFunc = this.judge; // for anonymous function below

    angular.element($window).on('keydown', function(e) {
      e.preventDefault();
      e.stopPropagation();

      if (e.originalEvent.code === "ArrowLeft") {
        judgeFunc(false);
      } else if (e.originalEvent.code === "ArrowRight") {
        judgeFunc(true);
      }
      console.log(e);
    });

  }]);
