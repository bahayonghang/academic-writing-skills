= Methods
== Encoding
Because the raw input remains unaligned, the encoder constructs a shared representation.
*Dynamic encoder.* Given the input sequence, the encoder extracts a dynamic representation.
*Candidate generator.* The representation conditions generation of candidate states.
*Candidate filter.* Remaining uncertainty determines which candidate states are retained.
$ z = f(x) $ <eq:encoder>
where $x$ is the input and $z$ is the latent state.
The state enters the candidate generator.
Training updates the encoder parameters.
== Decoding
Because the candidate state remains uncalibrated, the decoder maps it to the final output.
