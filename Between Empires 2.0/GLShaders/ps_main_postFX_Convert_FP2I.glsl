
varying float2 texCoord0;
varying float2 texCoord1;
varying float2 texCoord2;
varying float2 texCoord3;

void main()
{
	float3 rt;

	rt  = texture2D(postFX_sampler4, texCoord0).rgb;
	rt += texture2D(postFX_sampler4, texCoord1).rgb;
	rt += texture2D(postFX_sampler4, texCoord2).rgb;
	rt += texture2D(postFX_sampler4, texCoord3).rgb;

	rt *= 0.25;
	rt *= HDRRangeInv;
	
	gl_FragColor = vec4(rt, 1.0);
}
