package designpatterns.java.factory;

public class Main {
    public static void main(String[] args) {
        ShapeFactory shapeFactory = new ShapeFactory();
        Shape circleShape = shapeFactory.getShape("Circle");
        circleShape.draw();
    }    
}
