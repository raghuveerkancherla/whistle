[![Build Status](https://travis-ci.org/raghuveerkancherla/whistle.png?branch=master)](https://travis-ci.org/raghuveerkancherla/whistle) whistle
=======

Whistle takes an api driven approach to building web applications. The core part of the framework is less than 200 lines of code. WhistleCRUD is an implementation of the core Whistle framework to achieve CRUD based API's.


    class BlogResource(BaseResource):

        class Meta:
            entity = BlogEntity
            entity_repo = BlogEntityRepo


    blog_resource = BlogResource()
    blog = blog_resource.get(id=1)
    updated_blog = blog_resource.update(title='new blog title')
    blog_resource.delete(id=1)

* * *

Whistle has 3 main components.
 1. Resource: Resources define the basic crud functionality by default. You are free to add more functions, but it is recommended that you think carefully before you do. More often than not, it leads to unnecessary pollution of the api.
 2. Entity: Defines the properties of an entity that will be exposed via the Resource. It is highly recommended that there are no functions on these objects. If any they must be simple functions that manipulate data on the object.
 3. ResourceRepo: The persistence layer. Takes care of saving an Entity. If you want to store data to a different data store, you will want to implement this layer for the data store of your choice.
