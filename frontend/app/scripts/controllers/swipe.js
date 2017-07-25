'use strict';

/**
 * @ngdoc function
 * @name tinderApp.controller:SwipeCtrl
 * @description Controller for the swiping page
 */
angular.module('tinderApp')
    .controller('SwipeCtrl', ['$scope', 'Recommendations', 'JudgeRecommendation', '$window', function($scope, Recommendations, JudgeRecommendation, $window) {

        this.loadNewRecommendations = () => {
            this.isLoading = true;
            Recommendations.get((data) => {
                this.isLoading = false;
                this.currentIndex = 0;
                this.recommendations = data;
                this.currentRecommendation = this.recommendations[0];
            });
        };

        this.init = () => {
            this.isLoading = false;
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
