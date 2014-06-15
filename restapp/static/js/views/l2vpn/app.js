define([ 'jquery'
       , 'underscore'
       , 'backbone'
       , 'views/l2vpn/form'
       , 'views/l2vpn/list'
       ], function($, _, Backbone, formView, listView) {

  return Backbone.View.extend({

    events: {
      // Captures all clicks in subviews
      'click [data-href]': 'onLinkClicked'
    }

  , initialize: function () {
      // Bind to url changes
      this.router = this.options.router
      this.listenTo(this.router, 'route', this.onRoute)
    }

  , onRoute: function (route, params) {

      // Execute route method if present
      if (_.isFunction(this[route])) {

        // Remove current view
        if (this.currentView) {
          this.currentView.remove()
        }

        // Executes list/create/update based on url
        this[route].apply(this, params)

        if (this.currentView) {
          // Render and attach current view
          this.$el.html(this.currentView.render().el)
        }
      }
    }

  , onLinkClicked: function (e) {
      var $link = $(e.currentTarget)
      e.preventDefault()
      this.router.navigate($link.data('href'), {trigger: true})
    }

  , list: function () {
      this.currentView = new listView({collection: this.collection})
    }

  , create: function () {
      this.currentView = new formView({collection: this.collection})
      this.listenTo(this.currentView, {
        'success reset': function () {
          this.router.navigate('/', {trigger: true})
        }
      }, this)
    }

  , edit: function (id) {
      var model = this.collection.get(id)
      if (model) {
        this.currentView = new formView({model: model})
        this.listenTo(this.currentView, {
          'success reset': function () {
            this.router.navigate('/', {trigger: true})
          }
        }, this)
      } else {
        // redirect to list if no model found
        this.router.navigate('/', {trigger: true})
      }
    }

  })


})
