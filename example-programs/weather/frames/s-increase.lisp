(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureCollection temperature-space conceptual-space goodness-space)
    :no_of_dimensions 1))
 
(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-increase-location-sub" :parent_concept pp-inessive-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-increase-location-sub" :parent_concept pp-inessive-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define increase-sentence-input
  (def-contextual-space :name "s-increase.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space time-space conceptual-space)))
(define increase-sentence-output
  (def-contextual-space :name "s-increase.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space time-space conceptual-space)))
(define increase-sentence
  (def-frame :name "s-increase" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureCollection location-sub-frame time-sub-frame)
    :concepts (StructureCollection)
    :input_space increase-sentence-input
    :output_space increase-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) increase-sentence-input))
    :parent_space increase-sentence-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) increase-sentence-input))
    :parent_space increase-sentence-input))
(define time-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept more-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space increase-sentence-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space increase-sentence-input
    :conceptual_space location-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept more-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) increase-sentence-input))
    :parent_space increase-sentence-input
    :conceptual_space conceptual-space))

(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) increase-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list vb-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "increase"
    :locations (list vb-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :abstract_chunk increase-word))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) increase-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) increase-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-5 :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))

(define vb-super-chunk
  (def-letter-chunk :name None
    :locations (list vb-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureCollection sentence-word-2)
    :right_branch (StructureCollection sentence-word-3)))
(define vb-super-chunk-label
  (def-label :start vb-super-chunk :parent_concept vb-concept
    :locations (list vb-location
		     (Location (list) increase-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureCollection sentence-word-4)
    :right_branch (StructureCollection sentence-word-5)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) increase-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureCollection vb-super-chunk)
    :right_branch (StructureCollection pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) increase-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) increase-sentence-output))
    :parent_space increase-sentence-output
    :left_branch (StructureCollection sentence-word-1)
    :right_branch (StructureCollection vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) increase-sentence-output))))

(def-relation :start label-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start relation-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start nn-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jj-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start jjr-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start rp-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)
(def-relation :start sentence-concept :end increase-sentence
  :is_bidirectional True :activation 1.0)