(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-allative-time-input
  (def-contextual-space :name "pp[to-time].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define pp-allative-time-output
  (def-contextual-space :name "pp[to-time].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define pp-allative-time
  (def-frame :name "pp[to-time]" :parent_concept pp-allative-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection early-time-concept late-time-concept)
    :input_space pp-allative-time-input
    :output_space pp-allative-time-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-allative-time-input))
    :parent_space pp-allative-time-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-allative-time-input))
    :parent_space pp-allative-time-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-time-input))
    :parent_space pp-allative-time-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-time-input))
    :parent_space pp-allative-time-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-allative-time-input))
    :parent_space pp-allative-time-input
    :conceptual_space time-space))

(define pp-word-1
  (def-letter-chunk :name "to"
    :locations (list prep-location
		     (Location (list) pp-allative-time-output))
    :parent_space pp-allative-time-output
    :abstract_chunk to))
(define pp-word-2
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-time-output))
    :parent_space pp-allative-time-output))
(define pp-word-2-grammar-label
  (def-label :start pp-word-2 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-allative-time-output))))
(define pp-word-2-meaning-label
  (def-label :start pp-word-2 :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-time-output))))

(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-allative-time-output))
    :parent_space pp-allative-time-output
    :left_branch (StructureCollection pp-word-1)
    :right_branch (StructureCollection pp-word-2)))

(def-relation :start label-concept :end pp-allative-time
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-allative-time
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-allative-time
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-allative-time
  :is_bidirectional True :activation 1.0)