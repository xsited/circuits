require.config({
  paths: {
    jquery: '../vendor/jquery-1.10.2.min'
  , underscore: '../vendor/underscore-1.5.2.min'
  , backbone: '../vendor/backbone-1.0.0.min'
  , text: '../vendor/require.text-2.0.10'
  }
, shim: {
    underscore: {exports: '_'}
  , backbone: {
      deps: ['underscore', 'jquery']
    , exports: 'Backbone'
    }
  }
})
