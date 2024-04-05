(define (domain robot)
    (:requirements :strips :typing)
    (:types object
            robot
            liquid
            temp
    )

    (:predicates
        (atLocation ?r - robot ?o - object)
        (isHolding ?r - robot ?o - object)
        (isPlacedAt ?o - object ?r - object)
        ; (noLocation ?r)
        ; (objectType ?o - object ?t - type)
        (isFridge ?o)
        (isMicrowave ?o)
        (isSinkBasin ?o)
        (receptacle ?o)
        (openable ?o)
        (pickupable ?o)
        (toggleable ?o)
        (dirtyable ?o)
        (isToggled ?o)
        (isOpen ?o)
        (isPickedUp ?o)
        (isDirty ?o)
        (breakable ?o)
        (canFillWithLiquid ?o)
        (isFilledWithLiquid ?o)
        (fillLiquid ?o - object ?l - liquid)
        (isColdSource ?o)
        (isHeatSource ?o)
        (temperature ?o - object ?t - temp)
        (sliceable ?o)
        (controlledObjects ?k ?o)
        ; (isInteractable ?o)
    )

    (:constants
        ; SinkBasin Fridge Microwave - type
        Cold Hot RoomTemp - temp
        Water Coffee Wine - liquid
    )

    (:action GotoObject
    :parameters (?r - robot ?to - object)
    :precondition (and
            (not (exists (?from - object) (atLocation ?r ?from)))
            )
    :effect (and
                (atLocation ?r ?to)
            )
    )

    (:action GotoObjectFrom
    :parameters (?r - robot ?from - object ?to - object)
    :precondition (and
            (atLocation ?r ?from)
            )
    :effect (and
                (atLocation ?r ?to)
                (not (atLocation ?r ?from))
            )
    )

    (:action PickUpObject
    :parameters (?r - robot ?from - object ?o - object)
    :precondition (and
            (receptacle ?from)
            (atLocation ?r ?from)
            (isPlacedAt ?o ?from)
            (pickupable ?o)
            (forall (?o1 - object) (not (isHolding ?r ?o1)))
            (or (not (openable ?from)) (isOpen ?from))
            )
    :effect (and
                (isPickedUp ?o)
                (isHolding ?r ?o)
                (not (isPlacedAt ?o ?from))
            )
    )

    (:action PutDownObject
    :parameters (?r - robot ?to - object ?o - object)
    :precondition (and
            (receptacle ?to)
            (atLocation ?r ?to)
            (isPickedUp ?o)
            (isHolding ?r ?o)
            (or (not (openable ?to)) (isOpen ?to))
            )
    :effect (and
                (isPlacedAt ?o ?to)
                (not (isHolding ?r ?o))
                (not (isPickedUp ?o))
            )
    )

    (:action ToggleObjectOn
    :parameters (?r - robot ?o - object)
    :precondition (and
            (atLocation ?r ?o)
            (toggleable ?o)
            (not (isToggled ?o))
            )
    :effect (and
                (isToggled ?o)
            )
    )

    (:action ToggleObjectOff
    :parameters (?r - robot ?o - object)
    :precondition (and
            (atLocation ?r ?o)
            (toggleable ?o)
            (isToggled ?o)
            )
    :effect (and
                (not (isToggled ?o))
            )
    )

    (:action OpenObject
    :parameters (?r - robot ?o - object)
    :precondition (and
            (atLocation ?r ?o)
            (openable ?o)
            (not (isOpen ?o))
            )
    :effect (and
                (isOpen ?o)
            )
    )

    (:action CloseObject
    :parameters (?r - robot ?o - object)
    :precondition (and
            (atLocation ?r ?o)
            (openable ?o)
            (isOpen ?o)
            )
    :effect (and
                (not (isOpen ?o))
            )
    )

    (:action CleanObject
    :parameters (?r - robot ?l - object ?o - object)
    :precondition (and
            ;(ObjectType ?l SinkBasin)
            (isSinkBasin ?l)
            (atLocation ?r ?l)
            (isPickedUp ?o)
            (isHolding ?r ?o)
            (dirtyable ?o)
            (isDirty ?o)
            )
    :effect (and
                (not (isDirty ?o))
            )
    )

    (:action HeatObject
    :parameters (?r - robot ?l - object ?o - object)
    :precondition (and
            ;(ObjectType ?l Microwave)
            (isMicrowave ?l)
            (atLocation ?r ?l)
            (isPlacedAt ?o ?l)
            (not (isOpen ?l))
            (isToggled ?l)
            )
    :effect (and
                (temperature ?o Hot)
                (not (isToggled ?l))
            )
    )

    (:action CoolObject
    :parameters (?r - robot ?l - object ?o - object)
    :precondition (and
            ;(ObjectType ?l Fridge)
            (isFridge ?l)
            (atLocation ?r ?l)
            (isPlacedAt ?o ?l)
            (not (isOpen ?l))
            )
    :effect (and
                (temperature ?o Cold)
            )
    )

)
