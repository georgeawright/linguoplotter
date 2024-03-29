(define grammar-distance-to-proximity 0.1)
(define grammar-concept
  (def-concept :name "grammar" :distance_function boolean_distance
    :instance_type LetterChunk))
(define grammar-space
  (def-conceptual-space :name "grammar" :parent_concept grammar-concept
    :no_of_dimensions 1 :is_basic_level True :is_symbolic True))
(define string-concept
  (def-concept :name "string" :distance_function boolean_distance
    :instance_type LetterChunk))
(define string-space
  (def-conceptual-space :name "string" :parent_concept string-concept
    :no_of_dimensions 1 :is_basic_level False :is_symbolic True))

(define sentence-location (Location (list (list 1)) grammar-space))
(define conjunction-location (Location (list (list 1)) grammar-space))
(define np-location (Location (list (list 2)) grammar-space))
(define vp-location (Location (list (list 3)) grammar-space))
(define ap-location (Location (list (list 4)) grammar-space))
(define rp-location (Location (list (list 5)) grammar-space))
(define pp-location (Location (list (list 6)) grammar-space))
(define nn-location (Location (list (list 7)) grammar-space))
(define v-location (Location (list (list 8)) grammar-space))
(define vb-location (Location (list (list 9)) grammar-space))
(define aux-location (Location (list (list 10)) grammar-space))
(define jj-location (Location (list (list 11)) grammar-space))
(define jjr-location (Location (list (list 12)) grammar-space))
(define rb-location (Location (list (list 13)) grammar-space))
(define cop-location (Location (list (list 14)) grammar-space))
(define prep-location (Location (list (list 15)) grammar-space))
(define det-location (Location (list (list 16)) grammar-space))
(define nsubj-location (Location (list (list 17)) grammar-space))
(define predicate-location (Location (list (list 18)) grammar-space))
(define conj-location (Location (list (list 19)) grammar-space))
(define pron-location (Location (list (list 20)) grammar-space))
(define null-location (Location (list (list 21)) grammar-space))

(define sentence-concept
  (def-concept :name "sentence" :locations (list sentence-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 4 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define conjunction-concept
  (def-concept :name "conjunction" :locations (list conjunction-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 4 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define np-concept
  (def-concept :name "np" :locations (list np-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define vp-concept
  (def-concept :name "vp" :locations (list vp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define ap-concept
  (def-concept :name "ap" :locations (list ap-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define rp-concept
  (def-concept :name "rp" :locations (list rp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-concept
  (def-concept :name "pp" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-allative-concept
  (def-concept :name "pp-allative" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-allative-time-concept
  (def-concept :name "pp-allative-time" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-allative-location-concept
  (def-concept :name "pp-allative-location" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-ablative-concept
  (def-concept :name "pp-ablative" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-ablative-time-concept
  (def-concept :name "pp-ablative-time" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-ablative-location-concept
  (def-concept :name "pp-ablative-location" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-directional-concept
  (def-concept :name "pp-directional" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-directional-time-concept
  (def-concept :name "pp-directional-time" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-directional-location-concept
  (def-concept :name "pp-directional-location" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-inessive-concept
  (def-concept :name "pp-inessive" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-inessive-time-concept
  (def-concept :name "pp-inessive-time" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-inessive-location-concept
  (def-concept :name "pp-inessive-location" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-time-concept
  (def-concept :name "pp-time" :locations (list pp-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :possible_instances (StructureSet pp-inessive-time-concept pp-directional-time-concept)
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define nn-concept
  (def-concept :name "nn" :locations (list nn-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define v-concept
  (def-concept :name "v" :locations (list v-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define vb-concept
  (def-concept :name "vb" :locations (list vb-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define jj-concept
  (def-concept :name "jj" :locations (list jj-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define jjr-concept
  (def-concept :name "jjr" :locations (list jjr-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define rb-concept
  (def-concept :name "rb" :locations (list rb-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define cop-concept
  (def-concept :name "cop" :locations (list cop-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define prep-concept
  (def-concept :name "prep" :locations (list prep-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define det-concept
  (def-concept :name "det" :locations (list det-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define nsubj-concept
  (def-concept :name "nsubj" :locations (list nsubj-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define predicate-concept
  (def-concept :name "predicate" :locations (list predicate-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define conj-concept
  (def-concept :name "conj" :locations (list conj-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 2 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pron-concept
  (def-concept :name "pronoun" :locations (list pron-location)
    :classifier (ProximityClassifier)
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :depth 1 :distance_function boolean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))

(define verb-space
  (def-conceptual-space :name "verb" :parent_concept vb-concept
    :no_of_dimensions 1 :is_basic_level True :is_symbolic True))
(define be-location (Location (list (list 1)) verb-space))
(define increase-location (Location (list (list 2)) verb-space))
(define decrease-location (Location (list (list 3)) verb-space))
(define expand-location (Location (list (list 4)) verb-space))
(define shrink-location (Location (list (list 5)) verb-space))
(define move-location (Location (list (list 6)) verb-space))
(define spread-location (Location (list (list 7)) verb-space))

(define the
  (def-letter-chunk :name "the" :parent_space grammar-space
    :locations (list det-location)))
(define is
  (def-letter-chunk :name "is" :parent_space grammar-space
    :locations (list cop-location)))
(define will
  (def-letter-chunk :name "will" :parent_space grammar-space
    :locations (list aux-location)))
(define be
  (def-letter-chunk :name "be" :parent_space grammar-space
    :locations (list vb-location be-location)))
(define temperatures
  (def-letter-chunk :name "temperatures" :parent_space grammar-space
    :locations (list nn-location)))
(define they
  (def-letter-chunk :name "they" :parent_space grammar-space
    :locations (list pron-location)))
(def-relation :start nsubj-concept :end they :conceptual_space grammar-space)
(define in
  (def-letter-chunk :name "in" :parent_space grammar-space
    :locations (list prep-location)))
(define on
  (def-letter-chunk :name "on" :parent_space grammar-space
    :locations (list prep-location)))
(define across
  (def-letter-chunk :name "across" :parent_space grammar-space
    :locations (list prep-location)))
(define from
  (def-letter-chunk :name "from" :parent_space grammar-space
    :locations (list prep-location)))
(define to
  (def-letter-chunk :name "to" :parent_space grammar-space
    :locations (list prep-location)))
(define between
  (def-letter-chunk :name "between" :parent_space grammar-space
    :locations (list prep-location)))
(define than
  (def-letter-chunk :name "than" :parent_space grammar-space
    :locations (list prep-location)))
(define and
  (def-letter-chunk :name "and" :parent_space grammar-space
    :locations (list conj-location)))
(define but
  (def-letter-chunk :name "but" :parent_space grammar-space
    :locations (list conj-location)))
(define then
  (def-letter-chunk :name "then" :parent_space grammar-space
    :locations (list conj-location)))
(define meanwhile
  (def-letter-chunk :name "meanwhile" :parent_space grammar-space
    :locations (list conj-location)))
(define comma
  (def-letter-chunk :name "," :parent_space grammar-space
    :locations (list (Location (list) grammar-space))))
(define fstop
  (def-letter-chunk :name "." :parent_space grammar-space
    :locations (list (Location (list) grammar-space))))
(define -er
  (def-letter-chunk :name "[b]er" :parent_space grammar-space
    :locations (list (Location (list) grammar-space))))
(define -wards
  (def-letter-chunk :name "[b]wards" :parent_space grammar-space
    :locations (list (Location (list) grammar-space))))
(define null
  (def-letter-chunk :name "" :parent_space grammar-space
    :locations (list null-location)))
