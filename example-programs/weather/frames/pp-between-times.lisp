(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space
    :locations (list (Location (list (list Nan)) time-space))))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space
    :locations (list (Location (list (list Nan)) time-space))))
(def-relation :start early-time-concept :end late-time-concept
  :parent_concept different-concept)
(define similarity-space-parent-concept
  (def-concept :name "" :is_slot True))
(define similarity-space
  (def-conceptual-space :name "" :parent_concept similarity-space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space size-space location-space)
    :no_of_dimensions Nan))

(define pp-directional-time-input
  (def-contextual-space :name "pp[between-times].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define pp-directional-time-output
  (def-contextual-space :name "pp[between-times].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space time-space)))
(define pp-directional-time
  (def-frame :name "pp[between-times]"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet early-time-concept late-time-concept)
    :input_space pp-directional-time-input
    :output_space pp-directional-time-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-directional-time-input))
    :parent_space pp-directional-time-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-directional-time-input))
    :parent_space pp-directional-time-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-input))
    :parent_space pp-directional-time-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-input))
    :parent_space pp-directional-time-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-directional-time-input))
    :parent_space pp-directional-time-input
    :conceptual_space time-space))
(define sameness-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list)) (list (list)) similarity-space)
		     (TwoPointLocation (list (list)) (list (list)) pp-directional-time-input))
    :conceptual_space similarity-space))

(define pp-word-1
  (def-letter-chunk :name "between"
    :locations (list prep-location
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output
    :abstract_chunk between))
(define pp-word-2
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output))
(define pp-word-2-grammar-label
  (def-label :start pp-word-2 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-directional-time-output))))
(define pp-word-2-meaning-label
  (def-label :start pp-word-2 :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-output))))
(define pp-word-3
  (def-letter-chunk :name "and"
    :locations (list conj-location
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output
    :abstract_chunk and))
(define pp-word-4
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output))
(define pp-word-4-grammar-label
  (def-label :start pp-word-4 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-directional-time-output))))
(define pp-word-4-meaning-label
  (def-label :start pp-word-4 :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-directional-time-output))))

(define conj-super-chunk
  (def-letter-chunk :name None
    :locations (list conj-location
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output
    :left_branch (StructureSet pp-word-3)
    :right_branch (StructureSet pp-word-4)))
(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output
    :left_branch (StructureSet pp-word-2)
    :right_branch (StructureSet conj-super-chunk)))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-directional-time-output))
    :parent_space pp-directional-time-output
    :left_branch (StructureSet pp-word-1)
    :right_branch (StructureSet np-super-chunk)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-directional-time-concept
    :locations (list pp-location
		     (Location (list) pp-directional-time-output))))

(def-relation :start less-time-concept :end pp-directional-time
  :is_bidirectional True :stable_activation 1.0)
