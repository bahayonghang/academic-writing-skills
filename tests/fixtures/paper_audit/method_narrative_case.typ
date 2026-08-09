= Methods
== Encoding
Next, we describe the encoder component.
*Dynamic encoder.* This module is used to extract a dynamic representation.
*Candidate generator.* The component aims to generate candidate states.
*Candidate filter.* The stage serves to retain candidate states.
$ z = f(x) $ <eq:encoder>
The transform yields a latent state.
The state enters the candidate generator.
Training updates the encoder parameters.
== Decoding
Because the candidate state remains uncalibrated, the decoder maps it to the final output.
