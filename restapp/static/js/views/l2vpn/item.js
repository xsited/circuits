define([ 'underscore'
       , 'config'
       , 'backbone'
       , 'text!templates/l2vpn/item.html'
       ], function(_, config, Backbone, itemTemplate) {

  return Backbone.View.extend({

    template: _.template(itemTemplate)

  , tagName: 'li'

  , events: {
      'click .js-delete': 'onClickDelete'
    }

  , initialize: function () {
      this.listenTo(this.model, 'destroy', this.remove)
    }

  , render: function () {
      this.$el.html(this.template({
        attrs: this.model.toJSON()
      }))
      return this
    }

  , onClickDelete: function (e) {
      e.preventDefault()
      if (window.confirm('Are you sure to delete this record?')) {
        this.model.destroy()
      }
    }

  })

})
