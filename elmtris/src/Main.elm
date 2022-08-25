module Main exposing (main)
import Browser
import Html exposing (Html,div,canvas)
import Html.Attributes exposing (tabindex, id, style)
import Html.Events
import Json.Decode
import Time
import Keyboard.Event exposing (KeyboardEvent, considerKeyboardEvent)
import Browser.Navigation exposing (Key)


--MAIN

main = 
  Browser.element
    {init = init, 
    view = view, 
    update = update,
    subscriptions = subscriptions}


--MODEL

type alias Model = 
  {matrix: List (List Int),
  controlledBlock: Maybe (List (List Int))
  }


init : () -> (Model, Cmd Msg)
init _ = 
  (Model (List.repeat 21 (List.repeat 10 0)) Nothing
  , Cmd.none
  )

clearBoard: () -> Model
clearBoard _ =
  {matrix = List.repeat 21 (List.repeat 10 0)
   , controlledBlock = Nothing
  }


--UPDATE

type Msg
  =Tick Time.Posix
  |HandleKeyboardEvent Direction

update: Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case (model.controlledBlock) of
    Nothing ->
      ({model | controlledBlock = Just (generateBlock ())}, Cmd.none)
    Just controlledBlock ->
      case msg of
        Tick time ->  
          ({model | controlledBlock = Just (moveBlock Down controlledBlock)}, Cmd.none)
        HandleKeyboardEvent dir ->
          ({model | controlledBlock = Just (moveBlock dir controlledBlock)}, Cmd.none)
    


--SUBSCRIPTIONS

subscriptions: Model -> Sub Msg
subscriptions model= 
  Time.every 100 Tick


-- VIEW

view: Model -> Html Msg
view model= 
  div
    [ Html.Events.on "keydown" <|
        Json.Decode.map HandleKeyboardEvent (considerKeyboardEvent keyToDirection)
    , tabindex 0
    , id "id-for-auto-focus"
    , (style "outline" "none" )
    ]
    [Html.text (Debug.toString model)]


keyToDirection: KeyboardEvent -> Maybe Direction
keyToDirection event =
  case event.keyCode of
    29 -> --keycode for A
      Just Left
    10 -> --keycode for S
      Just Down
    33 -> --keycode for D
      Just Left
    78 -> --keycode for W
      Just AntiTrig
    20 -> --keycode for Q
      Just Trig

--MOVEMENT LOGIC

type Direction 
  =Left
  |Right
  |Down
  |Trig
  |AntiTrig

moveBlock: Direction -> List (List Int) -> List (List Int)
moveBlock dir current =
  case dir of
    Left ->
      List.map moveSquareLeft current
    Right ->
      List.map moveSquareRight current
    Down ->
      List.map moveSquareDown current
    Trig ->
      List.map (rotation90 (List.head current)) current
    AntiTrig ->
      List.map (rotation270 (List.head current)) current

moveSquareLeft: List Int -> List Int
moveSquareLeft square =
  [List.head square -1, List.tail square]

moveSquareRight: List Int -> List Int
moveSquareRight square =
  [List.head square + 1, List.tail square]

moveSquareDown: List Int -> List Int
moveSquareDown square =
  [List.head square, List.tail square + 1]

rotation90: List Int -> List Int -> List Int
rotation90 center square =
  [List.head center - List.tail square + List.tail center
  , List.tail center + List.head square - List.head square]

rotation270: List Int -> List Int -> List Int
rotation270 center square =
  [List.head center + List.tail square - List.tail center
  , List.tail center - List.head square + List.head square]


--BLOCKS

generateBlock: () -> List (List Int)
generateBlock _ =
  [[0,4],[0,5],[0,6],[1,4]]
  