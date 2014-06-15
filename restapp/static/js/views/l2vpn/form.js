define([ 'underscore'
       , 'config'
       , 'views/validation-form'
       , 'text!templates/l2vpn/form.html'
       ], function(_, config, ValidationFormView, l2vpnFormTemplate) {

  return ValidationFormView.extend({

    template: _.template(l2vpnFormTemplate)

  , render: function () {
      this.$el.html(this.template({
        config: config
      , hasModel: this.hasModel()
      , attrs: this.hasModel() ? this.model.toJSON() : {encapsulationtype: 2}
      }))
      return this
    }

  })

})
