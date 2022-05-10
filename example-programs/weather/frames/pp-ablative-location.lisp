(define early-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define late-location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-ablative-location-input
  (def-contextual-space :name "pp[from-location].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space)))
(define pp-ablative-location-output
  (def-contextual-space :name "pp[from-location].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space time-space)))
(define pp-ablative-location
  (def-frame :name "pp[from-location]" :parent_concept pp-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection early-location-concept late-location-concept
				   early-time-concept late-time-concept)
    :input_space pp-ablative-location-input
    :output_space pp-ablative-location-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define early-chunk-location-label
  (def-label :start early-chunk :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define late-chunk-location-label
  (def-label :start late-chunk :parent_concept late-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-location-input))
    :parent_space pp-ablative-location-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-ablative-location-input))
    :conceptual_space time-space))

(define pp-word-1
  (def-letter-chunk :name "from"
    :locations (list prep-location
		     (Location (list) pp-ablative-location-output))
    :parent_space pp-ablative-location-output
    :abstract_chunk from))
(define pp-word-2
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-ablative-location-output))
    :parent_space pp-ablative-location-output
    :abstract_chunk the))
(define pp-word-3
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-location-output))
    :parent_space pp-ablative-location-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word-3 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-ablative-location-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word-3 :parent_concept early-location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-ablative-location-output))))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-ablative-location-output))
    :parent_space pp-ablative-location-output
    :left_branch (StructureCollection pp-word-2)
    :right_branch (StructureCollection pp-word-3)))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-ablative-location-output))
    :parent_space pp-ablative-location-output
    :left_branch (StructureCollection pp-word-1)
    :right_branch (StructureCollection np-super-chunk)))

(def-relation :start label-concept :end pp-ablative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-ablative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-ablative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-ablative-location
  :is_bidirectional True :activation 1.0)
