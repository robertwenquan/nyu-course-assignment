#!/usr/bin/python

def get_text(name):
   return "lorem ipsum, {0} dolor sit amet".format(name)

def p_decorate(func):
   def func_wrapper(name):
       return "<p>{0}</p>".format(func(name))
   return func_wrapper

my_get_text = p_decorate(get_text)

print my_get_text("John")



@p_decorate
def get_text2(name):
   return "hello, {0} good bye".format(name)

print get_text2("John")


def strong_decorate(func):
    def func_wrapper(name):
        return "<strong>{0}</strong>".format(func(name))
    return func_wrapper

def div_decorate(func):
    def func_wrapper(name):
        return "<div>{0}</div>".format(func(name))
    return func_wrapper



@div_decorate
@p_decorate
@strong_decorate
def get_text3(name):
   return "hey, {0} how are you".format(name)

print get_text3("Jake")


