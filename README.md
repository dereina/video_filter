
ControllerInterface(abstract)
    abstract class to be implemented for the ui to interact with a controller that also implements the interface

    UI(ControllerInterface)
        Implements the ControllerInterface and acts as a bridge between the UI and the controller. Defines basics for building the UI

    VideoController(ControllerInterface)
        Implements the ControllerInterface and can work with an UI that also implements the ControllerInterface. Owns a VideoFilter that provides the logic to be executed from the UI

Component(abstract)
    abstract class for parsing UI configurations
    
    Slider(Component)
        Slider builder class


VideoUI(UI)
    Implementation of the UI with the creation of elements to interact with a VideoController 

Filter(abstract)
    Abstract class to implement a filter pass

VideoFilter
    Logic of the application
