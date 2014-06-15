define(['jquery', 'underscore'], function ($, _) {

  return {

    /*
     * Extracts errors from xhr
     */
    parseErrors: function (xhr) {
      var errors, note
      try {
        errors = $.parseJSON(xhr.responseText);
      } catch (e) {
        note = _.has(xhr, 'status') ? xhr.status : ''
        if (_.has(xhr, 'statusText')) note += ' ' + xhr.statusText
        errors = [{note: note || 'Application error'}]
      }
      return errors
    }

    /**
     *  Serializes form to object
     */
  , serializeObject: function(element) {
      var params = $(element).serializeArray()
        , o = {}

      $.each(params, function() {
        if (this.name in o) {
          if (!$.isArray(o[this.name])) {
            o[this.name] = [o[this.name]]
          }
          o[this.name].push(this.value)
        } else {
          o[this.name] = this.value
        }
      })
      return o
    }

  }

})
