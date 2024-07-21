# UML Diagrams
## TLDR (easy peasy) -
![alt text](images\image-10.png)

This class diagram represents a simplified model of an order processing system. Here's a breakdown of its components:

### Classes and Attributes:
1. **Customer**
   - Attributes: `name` (String), `address` (String)

2. **Order**
   - Attributes: `date` (date), `status` (String)
   - Operations: 
     - `calcSubTotal()`
     - `calcTax()`
     - `calcTotal()`
     - `calcTotalWeight()`

3. **OrderDetail**
   - Attributes: `quantity` (int), `taxStatus` (String)
   - Operations: 
     - `calcSubTotal()`
     - `calcWeight()`
     - `calcTax()`

4. **Item**
   - Attributes: `shippingWeight` (float), `description` (String)
   - Operations: 
     - `getPriceForQuantity()`
     - `getTax()`
     - `inStock()`

5. **Payment** (Abstract Class)
   - Attribute: `amount` (float)

6. **Cash** (inherits from Payment)
   - Attribute: `cashTendered` (float)

7. **Check** (inherits from Payment)
   - Attributes: `name` (String), `bankID` (String)
   - Operation: `authorized()`

8. **Credit** (inherits from Payment)
   - Attributes: `number` (String), `type` (String), `expDate` (String)
   - Operation: `authorized()`

### Relationships:
1. **Association**
   - Between `Customer` and `Order`: A customer can place multiple orders (`0..*`), but an order is placed by exactly one customer (`1`).

2. **Aggregation**
   - Between `Order` and `OrderDetail`: An order consists of multiple order details (`1..*`), where each order detail is part of one order (`1`).

3. **Association**
   - Between `OrderDetail` and `Item`: An order detail refers to one item (`1`), but an item can be part of multiple order details (`0..*`).

4. **Generalization**
   - Between `Payment` and its subclasses (`Cash`, `Check`, `Credit`): Payment is an abstract class, and the subclasses represent specific types of payment methods.

### Multiplicity:
- Specifies the number of instances in a relationship.
  - For example, the multiplicity `0..*` between `Customer` and `Order` indicates a customer can have zero or more orders.

### Key Points:
- **Attributes**: Properties or characteristics of a class.
- **Operations**: Functions or methods associated with a class.
- **Abstract Class**: A class that cannot be instantiated and usually contains one or more abstract methods that must be implemented by subclasses.
- **Generalization**: Indicates inheritance, where subclasses inherit attributes and operations from their parent class.
- **Aggregation**: A special form of association that represents a whole-part relationship.
- **Multiplicity**: Indicates how many instances of one class can be associated with instances of another class.

This diagram captures the structure and relationships of an order processing system, providing a clear overview of the entities involved and their interactions.

____

- Unified Modeling Language (UML) is a standard way to visualize the design of a software system.

- Among the many diagrams offered by UML, class diagrams are perhaps the most widely used.

- UML class diagram provides a static view of an object oriented system, showcasing its classes, attributes, methods, and the relationships among objects.

>This is the UML Diagram of Cat Class
![alt text](images\image.png)

![alt text](images\image-1.png)

Say you have a cat named Oscar. Oscar is an object, an instance
of the Cat class. Every cat has a lot of standard attributes:
name, sex, age, weight, color, favorite food, etc. These are the
class’s fields.

Luna, your friend’s cat, is also an instance of the Cat class.
It has the same set of attributes as Oscar. The difference is in
values of these attributes: her sex is female, she has a different
color, and weighs less.

So a class is like a blueprint that defines the structure for
objects, which are concrete instances of that class.

----
### Class hierarchies - 
Say your neighbor has a dog called Fido. It turns out, dogs
and cats have a lot in common: *name, sex, age, and color* are
attributes of both dogs and cats. Dogs can breathe, sleep and
run the same way cats do. So it seems that we can define the
base **Animal** class that would list the common attributes and
behaviors.

A parent class, like the one we’ve just defined, is called a
**superclass**. Its children are **subclasses**. Subclasses inherit state
and behavior from their parent, defining only attributes or
behaviors that differ. Thus, the `Cat` class would have the
`meow` method, and the `Dog` class the `bark` method.

>### UML diagram of a class hierarchy. All classes in this diagram are part of the `Animal` class hierarchy.
![alt text](images\image-2.png)

----

Imagine that you have a **FlyingTransport** interface with a method **fly(origin, destination, passengers)** .
When designing an air transportation simulator, you could restrict the **Airport** class to work only with objects that implement the **FlyingTransport** interface. After this, you can be sure that any object passed to an airport object, whether it’s an `Airplane` , a `Helicopter` or a freaking `DomesticatedGryphon` would be able to arrive or depart from this type of airport.

>### UML diagram of several classes implementing an interface.
![alt text](images\image-3.png)

----
>### UML diagram of extending a single class versus implementing multiple interfaces at the same time.
![alt text](images\image-4.png)

Here, `Animal` is a superclass, and `Cat` is a subclass and `Cat` class is implementing two interfaces: **FourLegged** and **OxygenBreathing** .

____

### PolyMorphism

Let’s look at some animal examples. Most `Animals` can make
sounds. We can anticipate that all subclasses will need to override
the base `makeSound` method so each subclass can emit
the correct sound; therefore we can declare it abstract right
away. This lets us omit any default implementation of the
method in the superclass, but force all subclasses to come up
with their own.

![alt text](images\image-5.png)

____
## Relations Between Objects

>### UML Association. Professor communicates with students.
![alt text](images\image-6.png)

Association is a type of relationship in which one object uses or
interacts with another. **In UML diagrams the association relationship
is shown by a simple arrow drawn from an object and pointing to the object it uses.** By the way, having a bi-directional association is a completely normal thing. In this case, the arrow has a point at each end.
>In general, you use an association to represent something like
a field in a class.

For example, a `Professor` object might have a field that is an array of `Student` objects. This is a one-to-many association because one professor can communicate with many students, but each student can communicate with only one professor.

____
>### UML Dependency. Professor depends on salary.
![alt text](images\image-7.png)

- Dependency is a weaker variant of association that usually implies that there’s no permanent link between objects.

- Dependency typically (but not always) implies that an object
accepts another object as a method parameter, instantiates, or
uses another object.

Here’s how you can spot a dependency between classes: a dependency exists between two classes if changes to the definition of one class result in modifications in another class.

____

>### UML Composition. University consists of departments.
![alt text](images\image-8.png)

Composition is a “whole-part” relationship between two objects, one of which is composed of one or more instances of the other.
____
>### UML Aggregation. Department contains professors
![alt text](images\image-9.png)
- Aggregation is a less strict variant of composition, where one object merely contains a reference to another. 
- The container doesn’t control the life cycle of the component. The component can exist without the container and can be linked to several containers at the same time.