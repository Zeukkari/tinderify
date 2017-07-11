'use strict';

describe('Controller: MatchCtrl', function() {

  // load the controller's module
  beforeEach(module('tinderApp'));

  var MatchCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function($controller, $rootScope) {
    scope = $rootScope.$new();
    MatchCtrl = $controller('MatchCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('Match list should be enabled', function() {
    expect(MatchCtrl.isMatchListEnabled).toBe(true);
  });

  it('Dates should be sorted in ascending order', function() {

    var messages = [{
      sent: 99
    }, {
      sent: 55
    }, {
      sent: 103
    }];
    var sorted = MatchCtrl.sortMessages(messages);
    expect(sorted[0].sent).toBe(55);
    expect(sorted[1].sent).toBe(99);
    expect(sorted[2].sent).toBe(103);

  });

  it('Match keys should be sorted according to date', function() {

    var matches = {
      "1": {
        id: "1",
        messages: [{
          sent: 2
        }]
      },
      "5": {
        id: "5",
        messages: [{
          sent: 9
        }]
      },
      "6": {
        id: "6",
        messages: []
      },

      "2": {
        id: "2",
        messages: [{
          sent: 3
        }]
      }
    };

    var sorted = MatchCtrl.sortMatchKeys(matches);

    expect(sorted[0]).toBe("5");
    expect(sorted[1]).toBe("2");
    expect(sorted[2]).toBe("1");
    expect(sorted[3]).toBe("6");


  });

  it('Verify matches are updated correctly', function() {

    var matches = {
      "1": {
        id: "1",
        messages: [{
          sent: 2,
          id: 1,
          message: "hi"
        }]
      },
      "2": {
        id: "2",
        messages: [{
          sent: 5,
          id: 2,
          message: "hello"
        }]
      },
    };

    MatchCtrl.processUpdates(matches);

    expect(MatchCtrl.matches["1"].id).toBe("1");
    expect(MatchCtrl.matches["1"].messages.length).toBe(1);

    matches["1"].messages.push({
      sent: 3,
      id: 2
    });

    MatchCtrl.processUpdates(matches);

    expect(MatchCtrl.matches["1"].id).toBe("1");
    expect(MatchCtrl.matches["1"].messages.length).toBe(2);
  });

  it('Chat view should be synced during updates', function() {

      var matches = {
        "1": {
          id: "1",
          messages: [{
            sent: 2,
            id: 1,
            message: "hi"
          }]
        }
      };

      MatchCtrl.currentMatch = {
        id: "1",
        messages: []
      };

      expect(MatchCtrl.currentMatch.messages.length).toBe(0);
      MatchCtrl.processUpdates(matches);
      MatchCtrl.processUpdates(matches);
      expect(MatchCtrl.currentMatch.messages.length).toBe(1);

    });

});
