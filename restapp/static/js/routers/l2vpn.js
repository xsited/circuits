define(['backbone'], function (Backbone) {

  return Backbone.Router.extend({

    routes: {
      '': 'list'
    , 'create': 'create'
    , ':id': 'view'
    , ':id/edit': 'edit'
    }

  , view: function (id) {
      // redirect to edit
      this.navigate(id + '/edit', {trigger: true})
    }

  })

})
