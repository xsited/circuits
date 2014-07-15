define([ 'underscore'
       , 'backbone'
       , 'utils'], function(_, Backbone, utils) {


  return Backbone.View.extend({

    events: {
      submit: 'onSubmit'
    , reset: 'onReset'
    }

    // Events

  , onSubmit: function(e) {
      e.preventDefault()
      e.stopPropagation()
      this._enterSyncState(function(){
        var attrs = this.getAttributes()
          , options = this.getOptions()

        if (this.hasModel()) {
          this.model.save(attrs, options)
        } else {
          this.collection.create(attrs, options)
        }
      })
    }

  , onReset: function(e) {
      e.stopPropagation()
      this.trigger('reset')
    }

  , onSuccess: function (model) {
      this._exitSyncState()
      this.trigger('success', model)
    }

  , onError: function (model, xhr) {
      var errors = utils.parseErrors(xhr)
      this._exitSyncState()
      this.trigger('error', model, errors)
    }

    // Getters

  , hasModel: function() { return !!this.model }

  , getOptions: function () {
      return { wait: true
             , success: _.bind(this.onSuccess, this)
             , error: _.bind(this.onError, this)
             }
    }

  , getAttributes: function () {
      return utils.serializeObject(this.getFormElement())
    }

  , getFormElement: function () {
      return this.$el.is('form') ? this.$el : this.$('form')
    }

    // Methods

  , submit: function () {
      this.getFormElement().trigger('submit')
      return this
    }

  , reset: function () {
      this.getFormElement().trigger('reset')
      return this
    }

    // Private

  , _enterSyncState: function (callback) {
      // Prevent double submit
      if (this._isSync) return this;
      this._isSync = true
      callback.call(this)
      return this
    }

  , _exitSyncState: function () {
      this._isSync = false
      return this
    }

  })

})

