App.module('Entities', function(Entities, App, Backbone, Marionette, $, _) {

    /**
     * Word item model
     *
     * @entity Word
     */
    Entities.Word = Backbone.Model.extend({
        defaults: {
            word: '',
            translation: '',
            strength: 0
        },

        urlRoot: function() {
            return '/api/user/words';
        },

        parse: function (response) {
            response.id = response["word_id"];
            delete response["word_id"];
            delete response["_id"];
            console.log(response);
            return response;
        },

        initialize: function(attributes, options) {
            options || (options = {});
            this.bind('error', this.defaultErrorHandler);
            this.init && this.init(attributes, options);
        },

        defaultErrorHandler: function(model, error) {
            if (error.status == 401 || error.status == 403 || error.status == 500) {
                App.vent.trigger('app:logout');
            }
        },

        validate: function(attrs, options) {
            var errors = {};
            if(!attrs.word) {
                errors.word = "Can't be blank";
            }
            if(!attrs.translation) {
                errors.translation = "Can't be blank";
            }
            if(!_.isEmpty(errors)) {
                return errors;
            }
        }
    });

    // Entities.configureStorage(Entities.Word);

    /**
     * Word items collection
     *
     * @entity Word
     */
    Entities.WordCollection = Backbone.Collection.extend({
        url: function() {
            return '/api/user/words';
        },

        model: Entities.Word,

        initialize: function(attributes, options) {
            options || (options = {});
            this.bind('error', this.defaultErrorHandler);
            this.init && this.init(attributes, options);
        },

        defaultErrorHandler: function(model, error) {
            if (error.status === 401 || error.status === 403 || error.status === 500) {
                App.vent.trigger('app:logout');
            }
        }
    });

    // Entities.configureStorage(Entities.WordCollection);

    /**
     * Initialize word items
     *
     * @entity Word
     */
    var initializeWords = function() {
        var words = new Entities.WordCollection([
            { 'id': 1, 'word': 'car', 'translation': 'auto', 'strength': 4 },
            { 'id': 2, 'word': 'house', 'translation': 'dom', 'strength': 5 },
            { 'id': 3, 'word': 'computer', 'translation': 'pocitac', 'strength': 2 },
            { 'id': 4, 'word': 'book', 'translation': 'kniha', 'strength': 3 }
        ]);

        return words.models;
    };

    /**
     * API
     * Main API methods for word entity
     */
    var API = {
        getWordsEntities: function() {
            var words = new Entities.WordCollection();
            var defer = $.Deferred();
            words.fetch({
                success: function(data) {
                    defer.resolve(data);
                }
            });
            var promise = defer.promise();
            return promise;
        },

        getWordEntity: function(wordId) {
            var word = new Entities.Word({id: wordId});
            var defer = $.Deferred();
            word.fetch({
                success: function(data) {
                    defer.resolve(data);
                },
                error: function(data) {
                    defer.resolve(undefined);
                }
            });
            return defer.promise();
        }
    };

    /**
     * Events
     */
    App.reqres.setHandler('words:entities', function() {
        return API.getWordsEntities();
    });

    App.reqres.setHandler('word:entity', function(id) {
        return API.getWordEntity(id);
    });

});
