x = {
  foo : function ()
  {
    console.log(this.state)
  },

  state:100
};

x.foo();

y = Object.create(x);
y.state = 99;
y.foo();

x.foo();

phantom.exit();

