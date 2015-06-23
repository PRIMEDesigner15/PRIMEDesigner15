/*function getLength(url) {
	return url.length
}
var audio = new Wad({
	source : 'testSong2.mp3',
	filter  : {
        type      : 'lowpass', // What type of filter is applied.
        frequency : 1000,       // The frequency, in hertz, to which the filter is applied.
        q         : 1,         // Q-factor.  No one knows what this does. The default value is 1. Sensible values are from 0 to 10.
        env       : {          // Filter envelope.
            frequency : 800, // If this is set, filter frequency will slide from filter.frequency to filter.env.frequency when a note is triggered.
            attack    : 0.5  // Time in seconds for the filter frequency to slide from filter.frequency to filter.env.frequency
        }
    },
})
audio.play({
		filter : {frequency : 90000000}
	})
*/