(define time-label-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-inessive-time-input
  (def-contextual-space :name "pp[in-time].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define pp-inessive-time-output
  (def-contextual-space :name "pp[in-time].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space time-space)))
(define pp-inessive-time
  (def-frame :name "pp[in-time]"
    :parent_concept pp-inessive-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet time-label-concept)
    :input_space pp-inessive-time-input
    :output_space pp-inessive-time-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))
(define time-relation
  (def-relation :start chunk :end chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input
    :conceptual_space time-space))
(define chunk-time-label
  (def-label :start chunk :parent_concept time-label-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))

(define pp-word-1
  (def-letter-chunk :name "on"
    :locations (list prep-location
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output
    :abstract_chunk on))
(define pp-word-2
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output))
(define pp-word-2-grammar-label
  (def-label :start pp-word-2 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-inessive-time-output))))
(define pp-word-2-meaning-label
  (def-label :start pp-word-2 :parent_concept time-label-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-output))))

(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output
    :left_branch (StructureSet pp-word-1)
    :right_branch (StructureSet pp-word-2)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-inessive-time-concept
    :locations (list pp-location
		     (Location (list) pp-inessive-time-output))))

(def-relation :start time-concept :end pp-inessive-time
  :is_bidirectional True :stable_activation 1.0)
