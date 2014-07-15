define([ 'backbone'
       , 'models/l2vpn'
       ], function (Backbone, L2vpnModel) {

  return Backbone.Collection.extend({
    model: L2vpnModel
  , url: '/api/l2vpn'
  })

})
