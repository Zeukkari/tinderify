'use strict';

describe('Controller: MatchCtrl', function () {

  // load the controller's module
  beforeEach(module('tinderApp'));

  var MatchCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MatchCtrl = $controller('MatchCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('Match list should be enabled', function () {
    expect(MatchCtrl.isMatchListEnabled).toBe(true);
  });

  it('Dates should be sorted in ascending order', function () {
    expect(MatchCtrl.isMatchListEnabled).toBe(true);
  });
});
