
uniform sampler2D postFX_sampler0;
uniform sampler2D postFX_sampler1;
uniform sampler2D postFX_sampler2;
uniform sampler2D postFX_sampler3;
uniform sampler2D postFX_sampler4;

uniform float4 color_value;
uniform float4 g_HalfPixel_ViewportSizeInv;
uniform float g_HDR_frameTime;	
uniform float g_DOF_Focus;
uniform float g_DOF_Range;
	
float CalculateWignette(float2 tc)
{
	tc = tc - 0.5; // [-1/2, 1/2]

	return pow(1.0 - dot(tc, tc), 4.0);
}

float4 radial(sampler2D tex, float2 texcoord, int samples, float startScale, float scaleMul)
{
    float4 c = vec4(0.0);
    float scale = startScale;
    for(int i = 0; i < samples; i++)
    {
        float2 uv = ((texcoord - 0.5) * scale) + 0.5;
        float4 s = texture2D(tex, uv);
        c += s;
        scale *= scaleMul;
    }

    c /= vec4(float(samples));
    return c;
}

float vignette(float2 pos, float inner, float outer)
{
	float r = dot(pos,pos);
	r = 1.0 - smoothstep(inner, outer, r);

	return r;
}

float3 tonemapping(float3 scene_color, float2 luminanceAvgMax, float tonemapOp)
{	
	float lum_avg = luminanceAvgMax.x * LuminanceAverageScaler; 
	float lum_max = luminanceAvgMax.y * LuminanceMaxScaler;
	
	const float MiddleValue = 0.85; 
	//float exposure = 1.4427 / (0.5 + lum_avg);
	float exposure = MiddleValue / (0.00001 + lum_avg);	
	exposure = clamp(exposure*HDRExposureScaler, min_exposure, max_exposure);
	
	float3 scene_color_exposed = scene_color * exposure;
	
	float3 final_color;
	{
		if( tonemapOp < 1.0 )
		{
			final_color = scene_color_exposed;
		}
		else if( tonemapOp < 2.0 )
		{
			final_color.rgb = 1.0 - exp2(-scene_color_exposed);
		}
		else if( tonemapOp < 3.0 )
		{
			final_color = scene_color_exposed / (scene_color_exposed + 1.0);
		}
		else //if( tonemapOp < 4.0 )
		{
			float Lp = (exposure / lum_avg) * max(scene_color_exposed.r, max(scene_color_exposed.g, scene_color_exposed.b));
			float LmSqr = lum_max; //(lum_max * lum_max) * (lum_max * lum_max);
			float toneScalar = ( Lp * ( 1.0 + ( Lp / ( LmSqr ) ) ) ) / ( 1.0 + Lp );

			final_color = scene_color_exposed * toneScalar;
		}
	}
	
	return final_color;
}

float4 ps_main_brightPass(bool with_luminance, float2 inTex)
{
	float3 color = texture2D(postFX_sampler0, inTex).rgb;
		
	//get real-range
	color *= HDRRange;
		
	//bright pass 
	if(with_luminance)	//use luminance information to calculate exposure factor to be applied on blur rt
	{
		float2 lum_avgmax = texture2D(postFX_sampler4, float2(0.5, 0.5)).rg;
		//color.rgb = tonemapping(color.rgb, lum_avgmax,0);//get exposed color
		const float MiddleValue = 0.85; 
		//float exposure = 1.4427 / (0.5 + lum_avg);
		float exposure_factor = MiddleValue / (0.00001 + lum_avgmax.x);	
		float exposure = 0.85 + exposure_factor * 0.15; 
		exposure = clamp(exposure*HDRExposureScaler, min_exposure, max_exposure);
		
		color.rgb = color.rgb * exposure;
		
		color.rgb = clamp((color.rgb - vec3(BrightpassTreshold)), 0.0, 100.0);
		float intensity = dot(color.rgb, vec3(0.5, 0.5, 0.5)) + 0.00001;
		float bloom_intensity = pow(intensity, BrightpassPostPower);
		color.rgb = color.rgb * (bloom_intensity / intensity);
	}
	else 
	{
		color.rgb = max(vec3(0.0), color.rgb - vec3(BrightpassTreshold));
		color.rgb = pow(color.rgb, vec3(BrightpassPostPower));
	}
	
	if(dot(color.rgb, color.rgb) > 1000.0) 
	{
		//avoid invalid flashes due to fp calc for nvidia cards..
		color.rgb = float3(0.0, 0.0, 0.0);
	}
	
	//we use interger format, turn back to normalized range
	color *= HDRRangeInv;
	
	return float4(color, 1.0);
}

float4 ps_main_postFX_AverageAvgMax(float2 texCoord, bool smooth_val)
{
	float offsets[4];
	offsets[0] = -1.5;
	offsets[1] = -0.5;
	offsets[2] = 0.5;
	offsets[3] = 1.5;
			
	float _max = 0.0;
	float _sum = 0.0;
	
	//downsample and find avg-max luminance
	for (int x = 0; x < 4; x++)
	{
		for (int y = 0; y < 4; y++)
		{
			float2 vOffset = float2(offsets[x], offsets[y]) * float2(g_HalfPixel_ViewportSizeInv.y, g_HalfPixel_ViewportSizeInv.w);
			float2 lumAvgMax_here = texture2D(postFX_sampler0, texCoord + vOffset).rg;
			
			_sum += lumAvgMax_here.r * lumAvgMax_here.r;
			_max = max(_max, lumAvgMax_here.g);
		}
	}

	float _avg = max(_sum / 16.0, 0.001); 

	float4 new_ret = float4(sqrt(_avg), _max, 0.0, 1.0);
	
	if(smooth_val)
	{
		//last step,  finish average luminance calculation
		new_ret.r = (new_ret.r);
		
		float2 prev_avgmax = texture2D(postFX_sampler4, float2(0.5, 0.5)).rg;
		
		//new_ret.xy = lerp(prev_avgmax, new_ret, /*1.0); //*/g_HDR_frameTime );
		new_ret.x = lerp(prev_avgmax.x, new_ret.x, g_HDR_frameTime );
		new_ret.y = max(0.1, lerp(prev_avgmax.y, new_ret.y, g_HDR_frameTime));
	}
	
	return max(vec4(0.0), new_ret);
}

float4 ps_main_postFX_DofBlur(bool using_hdr, bool using_depth, float2 texCoord)
{
	float3 sample_start = texture2D(postFX_sampler0, texCoord).rgb;

	float depth_start;
	if(using_depth)
	{
		depth_start = texture2D(postFX_sampler1, texCoord).r;
	}
	
	const int SAMPLE_COUNT = 8;
	float2 offsets[SAMPLE_COUNT];
	offsets[0] = vec2(-1.0, -1.0);
	offsets[1] = vec2(0.0, -1.0);
	offsets[2] = vec2(1.0, -1.0);
	offsets[3] = vec2(-1.0, 0.0);
	offsets[4] = vec2(1.0, 0.0);
	offsets[5] = vec2(-1.0, 1.0);
	offsets[6] = vec2(0.0, 1.0);
	offsets[7] = vec2(1.0, 1.0);
	
	float sampleDist = g_HalfPixel_ViewportSizeInv.x * 3.14;
	float3 sample_val = sample_start;
	float2 sample_pos;

	for (int i = 0; i < SAMPLE_COUNT; i++)
	{
		sample_pos = texCoord + vec2(sampleDist) * offsets[i];
		
		// !using_hdr -> non-lineer gamma!
		float3 sample_here;
		float depth_here;
		if(using_depth)
		{	
			depth_here = texture2D(postFX_sampler1, sample_pos).r;
			if(depth_here < depth_start) 
			{
				sample_here = sample_start;
			}
			else
			{
				sample_here = texture2D(postFX_sampler0, sample_pos).rgb;
			}
		}
		else
		{
			sample_here = texture2D(postFX_sampler0, sample_pos).rgb;
		}
		
		sample_val += sample_here;
	}

	sample_val /= float(SAMPLE_COUNT) + 1.0;

	return float4(sample_val, 1.0);
}

float4 FinalScenePassPS(bool use_dof, int use_hdr, bool use_auto_exp, float2 texCoord)
{
	// Sample the scene
	float4 scene = texture2D(postFX_sampler0, texCoord);
	scene.rgb = INPUT_OUTPUT_GAMMA(scene.rgb);
	
	#ifndef ENABLE_EDITOR	//we disable dof in editor mode so that we can fit in ps 2.0
		if(use_dof)
		{
			float pixelDepth = texture2D(postFX_sampler4, texCoord).r;
			float focus_factor01 = abs(g_DOF_Focus - pixelDepth);
			float lerp_factor = min(saturate(g_DOF_Range * focus_factor01), 0.62);

			const bool use_wignette = true;
			if(use_wignette)
			{
				lerp_factor *= 1.0 - vignette(float2(texCoord.x * 2.0 - 1.0, texCoord.y - 0.6), 0.015, 0.5); //remove blur from center
			}

			float4 dofColor = texture2D(postFX_sampler3, texCoord);

			if(use_hdr > 0)
			{
				dofColor *= HDRRange;
			}

			dofColor.rgb = INPUT_OUTPUT_GAMMA(dofColor.rgb);
			
			scene = lerp(scene, dofColor, lerp_factor);
		}
	#endif
	
	float4 color, blur;
	
	if(use_hdr > 0)
	{
		blur = texture2D(postFX_sampler1, texCoord);
		blur.rgb = pow(blur.rgb, vec3(BlurStrenght));
		
		blur.rgb *= HDRRange;
			
		float2 luminanceAvgMax;
		if(use_auto_exp)
		{
			luminanceAvgMax = texture2D(postFX_sampler2, float2(0.5, 0.5)).rg;
		}
		else
		{
			luminanceAvgMax = float2(0.5, 10.2);
		}
		
		// tonemap.. 
		color = scene; 
		
		color += blur * BlurAmount;
		color.rgb = tonemapping(color.rgb, luminanceAvgMax, postfxTonemapOp);
	}
	else
	{
		color = scene;
	}
	
	//gamma correction
	color.rgb = OUTPUT_GAMMA(color.rgb);
	
	return color;
}
