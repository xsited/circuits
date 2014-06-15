define([ 'underscore'
       , 'backbone'
       , 'views/l2vpn/item'
       , 'text!templates/l2vpn/list.html'
       ], function(_, Backbone, ItemView, listTemplate) {

  return Backbone.View.extend({

    template: _.template(listTemplate)

  , render: function () {
      this.$el.html(this.template())
      this.collection.each(this.addItem, this)
      return this
    }

  , addItem: function (item) {
      this.$('.js-items').append(new ItemView({model: item}).render().el)
    }

  })

})
