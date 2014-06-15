define([ 'underscore'
       , 'utils'
       , 'views/form'
       ], function(_, utils, FormView) {


  var Super = FormView.prototype

  return FormView.extend({

    showErrors: function (errors) {
      this.$('.js-error').each(function () {
        var $errorEl = $(this)
            // filter errors for field
          , fieldErrors = _.where(errors, {name: $errorEl.data('for')})
            // collect notes
          , notes = _.map(fieldErrors, function (error) {return error.note})
        if (notes.length > 0) {
          $errorEl.html(notes.join('<br>')).removeClass('is-hidden')
        } else {
          $errorEl.empty().addClass('is-hidden')
        }
      })
      return this
    }

  , hideErrors: function () {
      this.$('.js-error').each(function () {
        var $errorEl = $(this)
        $errorEl.empty().addClass('is-hidden')
      })
      return this
    }

    // Override base class

  , onReset: function (e) {
      this.hideErrors()
      Super.onReset.apply(this, arguments)
    }

  , onSuccess: function (model) {
      this.hideErrors()
      this.$(':input').removeAttr('disabled') // enable all fields
      Super.onSuccess.apply(this, arguments)
    }

  , onError: function (model, xhr) {
      var errors = utils.parseErrors(xhr)
      this.$(':input').removeAttr('disabled') // enable all fields
      this.showErrors(errors)
      Super.onError.apply(this, arguments)
    }

  , onSubmit: function (e) {
      Super.onSubmit.apply(this, arguments)
      this.$(':input').attr('disabled', true) // disable all fields
    }


  })


})
