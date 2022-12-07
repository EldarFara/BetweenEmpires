
uniform float alpha_test_val;
uniform float fShadowMapNextPixel;

#ifndef USE_ShadowTexelPos_INTERPOLATOR
uniform float fShadowMapSize;
#endif

float4 get_ambientTerm(int ambientTermType, float3 normal, float3 DirToSky, float sun_amount)
{
	float4 ambientTerm;
	if(ambientTermType == 0)	//constant
	{
		ambientTerm = vAmbientColor;
	}
	else if(ambientTermType == 1)	//hemisphere
	{
		float4 g_vGroundColorTEMP = vGroundAmbientColor * sun_amount;
		float4 g_vSkyColorTEMP = vAmbientColor;
		
		float lerpFactor = (dot(normal, DirToSky) + 1.0) * 0.5;
		
		float4 hemiColor = lerp( g_vGroundColorTEMP, g_vSkyColorTEMP, lerpFactor);
		ambientTerm = hemiColor;
	}
	else //if(ambientTermType == 2)	//ambient cube 
	{
		float4 cubeColor = textureCube(CubicTextureSampler, normal);
		ambientTerm = vAmbientColor * cubeColor;
	}
	return ambientTerm;
}

#ifdef USE_ShadowTexelPos_INTERPOLATOR
float GetSunAmount(int PcfMode, float4 ShadowTexCoord, float2 ShadowTexelPos)
#else
float GetSunAmount(int PcfMode, float4 ShadowTexCoord)
#endif
{
	float sun_amount = 0.0;
	if (PcfMode == PCF_NVIDIA)
	{
		sun_amount = saturate(sun_amount + texture2DProj(ShadowmapTextureSampler, ShadowTexCoord).r);
	}
	else
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float2 lerps = frac(ShadowTexelPos);
		#else
			float2 lerps = frac(ShadowTexCoord.xy * fShadowMapSize);
		#endif

		//read in bilerp stamp, doing the shadow checks
		float sourcevals[4];
		sourcevals[0] = (texture2D(ShadowmapTextureSampler, ShadowTexCoord.xy).r < ShadowTexCoord.z) ? 0.0: 1.0;
		sourcevals[1] = (texture2D(ShadowmapTextureSampler, (ShadowTexCoord.xy + float2(fShadowMapNextPixel, 0))).r < ShadowTexCoord.z) ? 0.0: 1.0;
		sourcevals[2] = (texture2D(ShadowmapTextureSampler, (ShadowTexCoord.xy + float2(0, fShadowMapNextPixel))).r < ShadowTexCoord.z) ? 0.0: 1.0;
		sourcevals[3] = (texture2D(ShadowmapTextureSampler, (ShadowTexCoord.xy + float2(fShadowMapNextPixel, fShadowMapNextPixel))).r < ShadowTexCoord.z) ? 0.0: 1.0;

		// lerp between the shadow values to calculate our light amount
		sun_amount = saturate(sun_amount + lerp(lerp(sourcevals[0], sourcevals[1], lerps.x), lerp(sourcevals[2], sourcevals[3], lerps.x), lerps.y));
	}

	return sun_amount;
}

float blurred_read_alpha(float2 texCoord)
{
	float sample_start = texture2D(CharacterShadowTextureSampler, saturate(texCoord)).r;
	
	const int SAMPLE_COUNT = 4;
	vec2 offsets[4];
	offsets[0] = vec2(-1.0, 1.0);
	offsets[1] = vec2(1.0, 1.0);
	offsets[2] = vec2(0.0, 2.0);
	offsets[3] = vec2(0.0, 3.0);
	
	float blur_amount = saturate(1.0 - texCoord.y);
	blur_amount *= blur_amount;
	float sampleDist = (6.0 / 256.0) * blur_amount;
	
	float sample_val = sample_start;
	
	for (int i = 0; i < SAMPLE_COUNT; i++)
	{
		float2 sample_pos = texCoord + sampleDist * offsets[i];
		float sample_here = texture2D(CharacterShadowTextureSampler, saturate(sample_pos)).r;
		sample_val += sample_here;
	}

	sample_val /= float(SAMPLE_COUNT) + 1.0;

	return sample_val;
}

float3 calculate_hair_specular(float3 normal, float3 tangent, float3 lightVec, float3 viewVec, float2 tc)
{
	// shift tangents
	float shiftTex = texture2D(Diffuse2Sampler, tc).a;
	
	float3 T1 = ShiftTangent(tangent, normal, specularShift.x + shiftTex);
	float3 T2 = ShiftTangent(tangent, normal, specularShift.y + shiftTex);

	float3 H = normalize(lightVec + viewVec);
	float3 specular = vSunColor.rgb * specularColor0 * HairSingleSpecularTerm(T1, H, specularExp.x);
	float3 specular2 = vSunColor.rgb * specularColor1 * HairSingleSpecularTerm(T2, H, specularExp.y);
	float specularMask = texture2D(Diffuse2Sampler, tc * 10.0).a;	// modulate secondary specular term with noise
	specular2 *= specularMask;
	float specularAttenuation = saturate(1.75 * dot(normal, lightVec) + 0.25);
	specular = (specular + specular2) * specularAttenuation;
	
	return specular;
}

PS_OUTPUT ps_main(VS_OUTPUT In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float sun_amount = 1.0; 
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	Output.RGBColor =  tex_col * (In.Color + (In.SunLight * sun_amount));

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;
		
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_standart(VS_OUTPUT_STANDART In, int PcfMode,  
	bool use_bumpmap, bool use_specularfactor, bool use_specularmap, bool ps2x, bool use_aniso, bool terrain_color_ambient,
	bool use_envmap, bool use_coloredspecmap, bool parallaxmapping_type)
{
	PS_OUTPUT Output;
	Output.RGBColor.w = 1.0;

	float3 normal;
	if(use_bumpmap)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0) - 1.0).xyz;
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
		
	//define ambient term:
	int ambientTermType = (terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0, 0.0, 1.0);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);	
	
	float3 aniso_specular = vec3(0.0);
	if(use_aniso)
	{
		float3 direction = float3(0.0, 1.0, 0.0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir : -vSunDir.xyz), In.ViewDir, In.Tex0);
	}
		
	if(use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.rgb;
	
		if(ps2x || !use_specularfactor)
		{
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING14
			if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
			{
				total_light.rgb += In.VertexLighting;
			}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			int effective_light_index = iLightIndices[0];
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index]  * light_atten);
		#endif
	}
	else
	{
		total_light.rgb += (saturate(dot(-vSunDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.rgb;
		
		if(ambientTermType != 1 && !ps2x)
		{
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
			total_light.rgb += In.VertexLighting;
		#endif
	}

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0);
		
	// Output.RGBColor.rgb = total_light.rgb;	//saturate?
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);

	if(ALPHA_TEST_ENABLED && (tex_col.a - alpha_test_val) < 0.0)
		discard;

	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor)
	{
		float4 fSpecular = vec4(0.0);
		
		float4 specColor = 0.1 * spec_coef * vec4(vSpecularColor.rgb, 1.0);

		if(use_specularmap)
		{
			float spec_tex_factor = dot(texture2D(SpecularTextureSampler, In.Tex0).rgb, vec3(0.33));	//get more precision from specularmap
			if(use_coloredspecmap)
			{
				float4 exponential = (specColor * 16.5);
				specColor = (Output.RGBColor * spec_tex_factor) * exponential;
			}
			else
			{
				specColor *= spec_tex_factor;
			}
		}
		else //if(use_specular_alpha)	//is that always true?
		{
			specColor *= tex_col.a;
		}
		
		//sun specular
		float3 vHalf = normalize(In.ViewDir + ((use_bumpmap) ?  In.SunLightDir : -vSunDir.xyz));
		
		float4 sun_specColor = specColor * vec4(vSunColor.rgb, 1.0) * sun_amount;		
		fSpecular = sun_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if (use_envmap)
		{
			float2 envpos;
			float3 tempvec = In.ViewDir.xyz - normal;

			envpos.x = (tempvec.y);// + tempvec.x);
			envpos.y = tempvec.z;
			envpos += 1.0;
			//   envpos *= 0.5;

			float2 envmap_tc = envpos;

			float3 envColor = texture2D(EnvTextureSampler, envmap_tc).rgb; // use .zw from the tex for the position of envmap
			if(use_coloredspecmap)
			{
				fSpecular.rgb += (specColor.rgb * envColor) * 0.039;
			}
			else
			{
				fSpecular.rgb += (specColor.rgb * envColor) * 0.035;
			}
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor.rgb * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE))
			{
				#ifndef USE_LIGHTING_PASS 
					//effective point light specular
					float light_atten = In.PointLightDir.a;
					int effective_light_index = iLightIndices[0];
					float4 light_specColor = specColor * vLightDiffuse[effective_light_index] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
					vHalf = normalize(In.ViewDir + In.PointLightDir.xyz);
					fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor.rgb * In.SkyLightDir * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = In.VertexColor.a;
	
	if(!use_specularfactor || !use_specularmap)
	{
		Output.RGBColor.a *= tex_col.a;
	}
	
	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	return Output;
}

PS_OUTPUT ps_main_standart_old_good(VS_OUTPUT_STANDART In, int PcfMode, bool use_specularmap, bool use_aniso)
{
	PS_OUTPUT Output;
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0) - 1.0).rgb;
	
	//define ambient term:
	const int ambientTermType = 1;
	float3 DirToSky = In.SkyLightDir;
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	float4 specColor = vec4(vSunColor.rgb, 1.0) * (vec4(vSpecularColor.rgb, 1.0) * 0.1);
	if(use_specularmap)
	{
		float spec_tex_factor = dot(texture2D(SpecularTextureSampler, In.Tex0).rgb, vec3(0.33));	//get more precision from specularmap
		specColor *= spec_tex_factor;
	}
	
	float3 vHalf = normalize(In.ViewDir + In.SunLightDir);
	float4 fSpecular = specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower); // saturate(dot(In.SunLightDir, normal));
	
	if(use_aniso)
	{
		float3 tangent_ = float3(0.0, 1.0, 0.0);
		fSpecular.rgb += calculate_hair_specular(normal, tangent_, In.SunLightDir, In.ViewDir, In.Tex0);
	}
	else
	{
		fSpecular.rgb *= spec_coef;
	}
		
	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + fSpecular) * sun_amount * vec4(vSunColor.rgb, 1.0);
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;	
	
	#ifndef USE_LIGHTING_PASS 
		float light_atten = In.PointLightDir.a;
		int effective_light_index = iLightIndices[0];
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vLightDiffuse[effective_light_index]  * light_atten;
	#endif
	
	#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
	#endif

	Output.RGBColor.rgb = total_light.rgb; //saturate(total_light.rgb);	//false!
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);

	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
		
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.a = In.VertexColor.a * tex_col.a;

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_bump(VS_OUTPUT_BUMP In, int PcfMode)
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;
	
	float3 normal;
	normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0).ag - 1.0);
	normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	
	if (PcfMode != PCF_NONE)
	{
		float sun_amount;
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount))) * vec4(vSunColor.rgb, 1.0);
	}
	else
	{
		total_light += saturate(dot(In.SunLightDir.xyz, normal.xyz)) * vec4(vSunColor.rgb, 1.0);
	}
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vec4(vPointLightColor.rgb, 1.0);
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;	
		
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_bump_simple(VS_OUTPUT_BUMP In, int PcfMode, bool use_parallaxmapping)
{ 
	PS_OUTPUT Output;

	if(ALPHA_TEST_ENABLED && (In.VertexColor.a - alpha_test_val) < 0.0)
		discard;
		
	 if (use_parallaxmapping)
	 {
		 float factor = (0.01 * vSpecularColor.x);
		 float BIAS = (factor * -0.5);//-0.02; 
		 float SCALE = factor;//0.04;

		 // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
		 float4 Normal = texture2D(NormalTextureSampler, In.Tex0);
		 float h = Normal.a * SCALE + BIAS;
		 In.Tex0.xy += h * Normal.z * In.ViewDir.xy; 
	 }
	
	float4 total_light = vAmbientColor;//In.LightAmbient;

	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);

	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vec4(vSunColor.rgb, 1.0);
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vec4(vPointLightColor.rgb, 1.0);
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
		
	float fresnel = 1.0 - (saturate(dot( In.ViewDir, In.WorldNormal)));

	Output.RGBColor.rgb *= max(0.6, fresnel * fresnel + 0.1);
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	if(Output.RGBColor.a < 0.05)
		discard;
	
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_bump_simple_multitex(VS_OUTPUT_BUMP In, int PcfMode, bool use_parallaxmapping)
{ 
	PS_OUTPUT Output;
		
	 if (use_parallaxmapping)
	 {
		 float factor = (0.01 * vSpecularColor.x);
		 float BIAS = (factor * -0.5);//-0.02; 
		 float SCALE = factor;//0.04;

		 // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
		 float4 Normal = texture2D(NormalTextureSampler, In.Tex0);
		 float h = Normal.a * SCALE + BIAS;
		 In.Tex0.xy += h * Normal.z * In.ViewDir.xy; 
	 }
	
	float4 total_light = vAmbientColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	float4 tex_col2 = texture2D(Diffuse2Sampler, In.Tex0 * uv_2_scale);
	
	float4 multi_tex_col = tex_col;
	float inv_alpha = (1.0 - In.VertexColor.a);
	multi_tex_col.rgb *= inv_alpha;
	multi_tex_col.rgb += tex_col2.rgb * In.VertexColor.a;
	
	//!!
	INPUT_TEX_GAMMA(multi_tex_col.rgb);

	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);

	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount)) * vec4(vSunColor.rgb, 1.0);
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vec4(vPointLightColor.rgb, 1.0);
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
		
	Output.RGBColor *= multi_tex_col;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	Output.RGBColor.a *= In.PointLightDir.a;	
	
	float fresnel = 1.0 - (saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
	Output.RGBColor.rgb *= max(0.6, fresnel*fresnel + 0.1);
		
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_flora(VS_OUTPUT_FLORA In, int PcfMode) 
{ 
	if(ALPHA_TEST_ENABLED && (In.Color.a - alpha_test_val) < 0.0)
		discard;

	PS_OUTPUT Output;
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	if (PcfMode != PCF_NONE)
	{
		float sun_amount;
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  tex_col * ((In.Color + float4(In.SunLight.rgb, 0.0) * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + float4(In.SunLight.rgb, 0.0)));
	}

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	if(Output.RGBColor.a < 0.1)
		discard;
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_flora_no_shadow(VS_OUTPUT_FLORA_NO_SHADOW In) 
{
	if(ALPHA_TEST_ENABLED && (In.Color.a - alpha_test_val) < 0.0)
		discard;

	PS_OUTPUT Output;
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_grass(VS_OUTPUT_FLORA In, int PcfMode) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = texture2D(GrassTextureSampler, In.Tex0);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	if ((PcfMode != PCF_NONE))
	{
		float sun_amount;
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  tex_col * (In.Color + (In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * (In.Color + In.SunLight);
	}

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_grass_no_shadow(VS_OUTPUT_FLORA_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;
		
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_envmap_specular(VS_OUTPUT_ENVMAP_SPECULAR In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 texColor = texture2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(texColor.rgb);
	
	float3 specTexture = texture2D(SpecularTextureSampler, In.Tex0.xy).rgb;
	float3 fSpecular = specTexture * In.vSpecular.rgb;

	float3 envColor = texture2D(EnvTextureSampler, In.Tex0.zw).rgb;
	
	if ((PcfMode != PCF_NONE))
	{
		
		float sun_amount;
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular) * sun_amount;
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight.rgb * sun_amount + 0.3) * (In.Color.rgb * envColor.rgb * specTexture);
	}
	else
	{
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular);
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight.rgb + 0.3) * (In.Color.rgb * envColor.rgb * specTexture);
	}	
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	Output.RGBColor.a = 1.0;
	
	if(bUseMotionBlur)
		Output.RGBColor.a = In.SunLight.a;
		
	return Output;
}

PS_OUTPUT ps_envmap_specular_singlespec(VS_OUTPUT_ENVMAP_SPECULAR In, int PcfMode)	//only differs by black-white specular texture usage
{
	PS_OUTPUT Output;
	
	// Compute half vector for specular lighting	
	float2 spectex_Col = texture2D(SpecularTextureSampler, In.Tex0.xy).ag;
	float specTexture = dot(spectex_Col, spectex_Col) * 0.5;
	float3 fSpecular = specTexture * In.vSpecular.rgb;
	
	float4 texColor = saturate( (saturate(In.Color + 0.5) * specTexture) * 2.0 + 0.25);

	float3 envColor = texture2D(EnvTextureSampler, In.Tex0.zw).rgb;

	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular) * sun_amount;
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight.rgb * sun_amount + 0.3) * (In.Color.rgb * envColor.rgb * specTexture);
	}
	else
	{
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular);
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight.rgb + 0.3) * (In.Color.rgb * envColor.rgb * specTexture);
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	Output.RGBColor.a = 1.0;

	return Output;
}

PS_OUTPUT ps_main_bump_interior(VS_OUTPUT_BUMP_DYNAMIC In)
{ 
    PS_OUTPUT Output;
    
    float4 total_light = vAmbientColor;//In.LightAmbient;
    
	#ifndef USE_LIGHTING_PASS
		float3 normal;
		normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));

		float LD = max(0.000001, dot(In.vec_to_light_0.xyz,In.vec_to_light_0.xyz));
		float3 L = normalize(In.vec_to_light_0.xyz);
		float wNdotL = dot(normal, L);

		total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[0]] / (LD);

		LD = dot(In.vec_to_light_1.xyz,In.vec_to_light_1.xyz);
		L = normalize(In.vec_to_light_1.xyz);
		wNdotL = dot(normal, L);
		total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[1]] /(LD);

		LD = dot(In.vec_to_light_2.xyz,In.vec_to_light_2.xyz);
		L = normalize(In.vec_to_light_2.xyz);
		wNdotL = dot(normal, L);
		total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[2]] /(LD);
	#endif

	Output.RGBColor = float4(total_light.rgb, 1.0);
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
    INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;	
		
    Output.RGBColor.rgb = saturate(OUTPUT_GAMMA(Output.RGBColor.rgb));
    Output.RGBColor.a = In.VertexColor.a;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

//uses standart-style normal maps
PS_OUTPUT ps_main_bump_interior_new(VS_OUTPUT_BUMP_DYNAMIC_NEW In, bool use_specularmap ) //ps_main_bump_interior with std normalmaps
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;

	// effective lights!?
	#ifndef USE_LIGHTING_PASS
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	
	float LD_0 = saturate(1.0 / max(0.000001, dot(In.vec_to_light_0.xyz,In.vec_to_light_0.xyz)));
	float3 L_0 = normalize(In.vec_to_light_0.xyz);
	float wNdotL_0 = dot(normal, L_0);
	total_light += saturate(wNdotL_0) * vLightDiffuse[ iLightIndices[0] ] * (LD_0);

	//	LD = In.vec_to_light_1.w;
	float LD_1 = saturate(1.0 / max(0.000001, dot(In.vec_to_light_1.xyz,In.vec_to_light_1.xyz)));
	float3 L_1 = normalize(In.vec_to_light_1.xyz);
	float wNdotL_1 = dot(normal, L_1);
	total_light += saturate(wNdotL_1) * vLightDiffuse[ iLightIndices[1] ] * (LD_1);

	//	LD = In.vec_to_light_2.w;
	float LD_2 = saturate(1.0 / max(0.000001, dot(In.vec_to_light_2.xyz,In.vec_to_light_2.xyz)));
	float3 L_2 = normalize(In.vec_to_light_2.xyz);
	float wNdotL_2 = dot(normal, L_2);
	total_light += saturate(wNdotL_2) * vLightDiffuse[ iLightIndices[2] ] * (LD_2);
	#endif
	
	//	Output.RGBColor = saturate(total_light * 0.6) * 1.66;
	Output.RGBColor = float4(total_light.rgb, 1.0);
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	if(use_specularmap)
	{
		float4 fSpecular = vec4(0.0);
		
		//light0 specular
		float4 light0_specColor = vLightDiffuse[ iLightIndices[0] ] * LD_0;
		float3 vHalf_0 = normalize(In.ViewDir + L_0);
		fSpecular = light0_specColor * pow( saturate(dot(vHalf_0, normal)), fMaterialPower);
				
		float4 specColor = 0.1 * spec_coef * vec4(vSpecularColor.rgb, 1.0);
		float spec_tex_factor = dot(texture2D(SpecularTextureSampler, In.Tex0).rgb, vec3(0.33));	//get more precision from specularmap
		specColor *= spec_tex_factor;
		
		Output.RGBColor += specColor * fSpecular;
	}	
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor = saturate(Output.RGBColor);
	Output.RGBColor.a = In.VertexColor.a;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_character_shadow(int PcfMode, VS_OUTPUT_CHARACTER_SHADOW In)
{ 
	PS_OUTPUT Output;

	if (PcfMode == PCF_NONE)
	{
		Output.RGBColor.a = blurred_read_alpha(In.Tex0) * In.Color.a;
	}
	else
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor.a = saturate(blurred_read_alpha(In.Tex0) * In.Color.a * sun_amount);
	}	
	
	Output.RGBColor.rgb = In.Color.rgb;
	
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_character_shadow_new(int PcfMode, VS_OUTPUT_CHARACTER_SHADOW In)
{ 
	PS_OUTPUT Output;
	
	if (PcfMode == PCF_NONE)
	{
		Output.RGBColor.a = texture2D(CharacterShadowTextureSampler, In.Tex0).r * In.Color.a;
	}
	else
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif

		Output.RGBColor.a = saturate(texture2D(CharacterShadowTextureSampler, In.Tex0).r * In.Color.a * sun_amount);
	}
	
	Output.RGBColor.rgb = In.Color.rgb;
	
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_water(VS_OUTPUT_WATER In, bool use_high, bool apply_depth, bool mud_factor)
{ 
	PS_OUTPUT Output;
	
	const bool rgb_normalmap = false; //!apply_depth;
	
	float3 normal;
	if(rgb_normalmap)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	}
	else
	{
		normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	}
	
	if(!apply_depth)
	{
		normal = float3(0.0, 0.0, 1.0);
	}
	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		float2 ref_tc = float2((0.25 * normal.xy) + float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.5 - 0.5 * (In.PosWater.y / In.PosWater.w)));
		tex = texture2D(ReflectionTextureSampler, float2(ref_tc.x, 1.0 - ref_tc.y));
	}
	else
	{
		//for objects use env map (they use same texture register)
		tex = texture2D(EnvTextureSampler, (vView - normal).yx * 3.4);
	}

	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01 * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125;
	}
	
	// Fresnel term
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);

	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01);
	}

	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160)*fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}

	Output.RGBColor.a = 1.0 - 0.3 * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0;
	}
	
	float3 g_cDownWaterColor = mud_factor ? float3(4.5/255.0, 8.0/255.0, 6.0/255.0) : float3(1.0/255.0, 4.0/255.0, 6.0/255.0);
	float3 g_cUpWaterColor   = mud_factor ? float3(5.0/255.0, 7.0/255.0, 7.0/255.0) : float3(1.0/255.0, 5.0/255.0, 10.0/255.0);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;

	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1;
		fog_fresnel_factor += 0.05;
	}

	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022, 0.02, 0.005) * (1.0 - saturate(dot(vView, normal)));
	}
	
	if(apply_depth && use_depth_effects)
	{
		float2 proj_uv = In.projCoord.xy / In.projCoord.w;
		float depth = texture2D(DepthTextureSampler, float2(proj_uv.x, 1.0 - proj_uv.y)).r;

		float alpha_factor;
		if((depth + 0.0005) < In.Depth)
		{
			alpha_factor = 1.0;
		}
		else
		{
			alpha_factor = saturate((depth - In.Depth) * 2048.0);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth) * 32.0);
		
		const bool use_refraction = false;
		
		if(use_refraction && use_high)
		{
			float4 coord_start = In.projCoord;
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1);
			float depth_here = texture2D(DepthTextureSampler, coord_disto.xy).r;
			float4 refraction;

			if(depth_here < depth)
				refraction = texture2DProj(ScreenTextureSampler, coord_disto);
			else
				refraction = texture2DProj(ScreenTextureSampler, coord_start);

			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			float val = saturate(1.0 - Output.RGBColor.w);
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, val * 0.55);

			if(Output.RGBColor.a > 0.1)
			{
				Output.RGBColor.a *= 1.75;
			}

			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25;
			}
		}
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0;
	}
	
	return Output;
}

PS_OUTPUT ps_hair(VS_OUTPUT_SIMPLE_HAIR In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex1_col = texture2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = texture2D(Diffuse2Sampler, In.Tex0);

	float4 final_col;
	
	INPUT_TEX_GAMMA(tex1_col.rgb);
	
	final_col = tex1_col * vMaterialColor;
	
	float alpha = saturate(((2.0 * vMaterialColor2.a ) + tex2_col.a) - 1.9);
	final_col.rgb *= (1.0 - alpha);
	final_col.rgb += tex2_col.rgb * alpha;
	
	float4 total_light = In.Color;
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		total_light.rgb += In.SunLight.rgb * sun_amount;
	}
	else
	{
		total_light.rgb += In.SunLight.rgb;
	}

	Output.RGBColor =  final_col * total_light;

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_hair_aniso(VS_OUTPUT_HAIR In, int PcfMode, bool no_blend)
{
	PS_OUTPUT Output;

	float3 lightDir = -vSunDir.xyz;
	float3 hairBaseColor = vMaterialColor.rgb;

	// diffuse term
	float3 diffuse = hairBaseColor * vSunColor.rgb * In.VertexColor.rgb * HairDiffuseTerm(In.normal, lightDir);

	float4 tex1_col = texture2D(MeshTextureSampler, In.Tex0);

	INPUT_TEX_GAMMA(tex1_col.rgb);
	
	float4 final_col = tex1_col;
	final_col.rgb *= hairBaseColor;
	
	if(!no_blend)
	{
		float4 tex2_col = texture2D(Diffuse2Sampler, In.Tex0);
		float alpha = saturate(((2.0 * vMaterialColor2.a ) + tex2_col.a) - 1.9);
	
		final_col.rgb *= (1.0 - alpha);
		final_col.rgb += tex2_col.rgb * alpha;
	}
		
	float sun_amount = 1.0;
	if ((PcfMode != PCF_NONE))
	{
		 #ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	
	float3 specular = calculate_hair_specular(In.normal, In.tangent, lightDir, In.viewVec, In.Tex0);
	
	float4 total_light = vAmbientColor;
	total_light.rgb += (((diffuse + specular) * sun_amount));
	
	total_light.rgb += In.VertexLighting.rgb;
	
	Output.RGBColor.rgb = total_light.rgb * final_col.rgb;
		
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	Output.RGBColor.a = tex1_col.a * vMaterialColor.a;

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	Output.RGBColor = saturate(Output.RGBColor);	//do not bloom!	
	
	return Output;
}

PS_OUTPUT ps_face(VS_OUTPUT_SIMPLE_FACE In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex1_col = texture2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = texture2D(Diffuse2Sampler, In.Tex0);
	
	float4 tex_col;
	
	tex_col = tex2_col * In.Color.a + tex1_col * (1.0 - In.Color.a);
	
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = tex_col * (In.Color + In.SunLight);
	}	

	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = vMaterialColor.a;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_standart_face_mod(VS_OUTPUT_STANDART In, int PcfMode, bool use_bumpmap, bool use_ps2a)
{ 
	PS_OUTPUT Output;

	float4 total_light = vAmbientColor;//In.LightAmbient;

	float3 normal;
	
	if(use_bumpmap)
	{
		float3 tex1_norm, tex2_norm;
		tex1_norm = texture2D(NormalTextureSampler, In.Tex0).rgb;
		
		if(use_ps2a)
		{
			//add old's normal map with ps2a 
			tex2_norm = texture2D(SpecularTextureSampler, In.Tex0).rgb;
			normal = lerp(tex1_norm, tex2_norm, In.VertexColor.a);	// blend normals different?
			normal = 2.0 * normal - 1.0;		
			normal = normalize(normal);
		}
		else
		{
			normal = (2.0 * tex1_norm - 1.0);
		}
	}
	else
	{
		normal = In.SunLightDir.xyz;
	}
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	
	if(use_bumpmap)
	{
		total_light += face_NdotL(In.SunLightDir.xyz, normal.xyz) * sun_amount * vec4(vSunColor.rgb, 1.0);
		if(use_ps2a)
		{
			total_light += face_NdotL(In.SkyLightDir.xyz, normal.xyz) * vSkyLightColor;
		}
	}
	else 
	{
		total_light += face_NdotL(-vSunDir.xyz, normal.xyz) * sun_amount * vec4(vSunColor.rgb, 1.0);

		if(use_ps2a)
		{
			total_light += face_NdotL(-vSkyLightDir.xyz, normal.xyz) * vSkyLightColor;
		}
	}

	float3 point_lighting = vec3(0.0);
	#ifndef USE_LIGHTING_PASS 
		float light_atten = In.PointLightDir.a * 0.9;
		int effective_light_index = iLightIndices[0];
		point_lighting += light_atten * face_NdotL(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index].xyz;
	#endif
	
	#ifdef INCLUDE_VERTEX_LIGHTING
		if(use_ps2a)
		{
			point_lighting += In.VertexLighting;
		}
	#endif

	total_light.rgb += point_lighting;

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0);

	float4 tex1_col = texture2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = texture2D(Diffuse2Sampler, In.Tex0);
	float4 tex_col = lerp(tex1_col, tex2_col, In.VertexColor.a);
	
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	Output.RGBColor *= tex_col;
	Output.RGBColor.rgb *= (In.VertexColor.rgb * vMaterialColor.rgb);
	
	if(use_ps2a)
	{
		float fSpecular = 0.0;
		
		float4 specColor =  vec4(vSpecularColor.rgb, 1.0) * vec4(vSunColor.rgb, 1.0);	//float4(1.0, 0.9, 0.8, 1.0) * 2;//
		
		float3 vHalf = normalize(In.ViewDir + In.SunLightDir);
		fSpecular = (specColor * pow(saturate(dot(vHalf, normal)), fMaterialPower) * sun_amount).x; 
		
		float fresnel = saturate(1.0 - dot(In.ViewDir, normal));
		Output.RGBColor += vec4(fresnel * fSpecular);
	}
		
	Output.RGBColor.rgb = saturate(OUTPUT_GAMMA(Output.RGBColor.rgb));	//do not bloom!
	Output.RGBColor.a = vMaterialColor.a;

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_depthed_flare(VS_DEPTHED_FLARE In, bool sun_like, bool blend_adding) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor *= texture2D(MeshTextureSampler, In.Tex0);

	if(!blend_adding)
	{
		//this shader replaces "ps_main_no_shadow" which uses gamma correction..
	
		Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
		OUTPUT_GAMMA(Output.RGBColor.rgb);
	}
	
	if(use_depth_effects)
	{
		//add volume to in.depth?
		float depth = texture2DProj(DepthTextureSampler, In.projCoord).r;
		
		float alpha_factor;
		
		if(sun_like)
		{
			float my_depth = 0.0;	//STR?: wignette like volume? tc!
			alpha_factor = depth;
			float fog_factor = 1.001 - (10.0 * (fFogDensity + 0.001));	//0.1 -> 0.0  & 0.01 -> 1.0
			alpha_factor *= fog_factor;
		}
		else
		{
			alpha_factor = saturate((depth - In.Depth) * 4096.0); 
		}
		
		if(blend_adding)
		{
			Output.RGBColor *= alpha_factor;	//pre-multiplied alpha
		}
		else
		{
			Output.RGBColor.a *= alpha_factor;
		}
	}
	
	return Output;
}

PS_OUTPUT ps_main_map(VS_OUTPUT_MAP In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float sun_amount = 1.0;
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	
	//add fresnel term
	{
		float fresnel = 1.0 - (saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
		fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6, fresnel + 0.1); 
	}	

	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_map_bump(VS_OUTPUT_MAP_BUMP In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0 * map_normal_detail_factor).rgb - 1.0);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor.rgb * vMaterialColor * vColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vec4(vSunColor.rgb, 1.0) * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1.0;
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	Output.RGBColor.rgb =  tex_col.rgb * ((In.Color.rgb + In_SunLight.rgb * sun_amount));
	Output.RGBColor.a = In.Color.a;
	
	//add fresnel term
	{
		float fresnel = 1.0 - (saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
		fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6, fresnel + 0.1); 
	}
		
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_mountain(VS_OUTPUT_MAP_MOUNTAIN In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	tex_col.rgb += saturate(In.Tex0.z * (tex_col.a) - 1.5);
	tex_col.a = 1.0;
	
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  saturate(tex_col) * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = saturate(tex_col) * (In.Color + In.SunLight);
	}
	
	Output.RGBColor.a = In.Color.a;
	
	{
		float fresnel = 1.0 - (saturate(dot( In.ViewDir, In.WorldNormal)));
	//	fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6, fresnel + 0.1); 
	}	
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_mountain_bump(VS_OUTPUT_MAP_MOUNTAIN_BUMP In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 sample_col = texture2D(MeshTextureSampler, In.Tex0.xy);
	
	INPUT_TEX_GAMMA(sample_col.rgb);
	float4 tex_col = sample_col;
	
	tex_col.rgb += saturate(In.Tex0.z * (sample_col.a) - 1.5);
	tex_col.a = 1.0;
	
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0.xy * map_normal_detail_factor).rgb - 1.0);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor.rgb;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vec4(vSunColor.rgb, 1.0);
	
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  saturate(tex_col) * ((In.Color + In_SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = saturate(tex_col) * (In.Color + In_SunLight);
	}
	
	{
		float fresnel = 1.0 - (saturate(dot( In.ViewDir, In.WorldNormal)));
		Output.RGBColor.rgb *= max(0.6, fresnel + 0.1); 
	}
	
	Output.RGBColor.a = In.Color.a;
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_water(bool reflections, VS_OUTPUT_MAP_WATER In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor = In.Color;

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float3 normal;
	normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0 * 8.0).ag - 1.0);
	normal.z = sqrt(max(0.000001, 1.0 - dot(normal.xy, normal.xy)));
	normal = normalize(normal);

	float NdotL = saturate(dot(normal, In.LightDir));
	float3 vView = normalize(In.CameraDir);

	// Fresnel term
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	Output.RGBColor.rgb += fresnel * In.Color.rgb;
		
	if(reflections)
	{
		In.PosWater.xy += 0.35 * normal.xy;
		float4 tex = texture2DProj(ReflectionTextureSampler, In.PosWater);
		INPUT_OUTPUT_GAMMA(tex.rgb);
		tex.rgb = min(tex.rgb, 4.0);
		Output.RGBColor.rgb *= NdotL * lerp(tex_col.rgb, tex.rgb, reflection_factor);
	}
	else
	{
		Output.RGBColor.rgb *= tex_col.rgb;
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	Output.RGBColor.a = In.Color.a * tex_col.a;
	
	return Output;
}

PS_OUTPUT ps_skybox_shading(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor *= texture2D(MeshTextureSampler, In.Tex0);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_skybox_shading_new(bool use_hdr, VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	
	if(use_hdr)
	{
		Output.RGBColor =  In.Color;
		Output.RGBColor *= texture2D(Diffuse2Sampler, In.Tex0);
		
		// expand to floating point.. (RGBE)
		float2 scaleBias = float2(vec4(vSpecularColor.rgb, 1.0).x, vec4(vSpecularColor.rgb, 1.0).y);
		
		float exFactor16 = texture2D(EnvTextureSampler, In.Tex0).r;
		float exFactor8 = floor(exFactor16 * 255.0) / 255.0;
		Output.RGBColor.rgb *= exp2(exFactor16 * scaleBias.x + scaleBias.y);
	}
	else
	{
		//switch to old style
		Output.RGBColor =  In.Color;
		float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
		INPUT_TEX_GAMMA(tex_col.rgb);
		Output.RGBColor *= tex_col;
	}
	
	Output.RGBColor.a = 1.0;
		
	//gamma correct?
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	if(In.Color.a == 0.0)
	{
		Output.RGBColor.rgb = saturate(Output.RGBColor.rgb);
	}

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_no_shadow_season(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	if((tex_col.a - 0.5) < 0.0)
	{
		discard;
	}
		
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb = saturate(tex_col.rgb * float3(0.9, 1.1, 0.9));
	}
	else if ((season > 0.5) && (season < 1.5)) //1= summer
	{
		tex_col.rgb = saturate(tex_col.rgb * float3(1.0, 1.0, 1.0));
	}
	else if ((season > 1.5) && (season < 2.5)) //2= autumn
	{
		tex_col.rgb = saturate(tex_col.rgb * float3(1.1, 0.9, 0.9));
	}
	else if (season > 2.5) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}

	Output.RGBColor = In.Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_no_shadow_season_bump(VS_OUTPUT_FONT_X_BUMP In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	if((tex_col.a - 0.5) < 0.0)
	{
		discard;
	}
		
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	float3 sky_light_dir = In.SkyDir;
	float3 sun_dir = In.SunDir;
	float4 vColor = In.vColor;
	
	//computation copy from vertex shader
	float4 Out_Color;
	{
		float lighting_factor = 1.0;
		float4 diffuse_light = vAmbientColor;
		diffuse_light += saturate(dot(normal, sky_light_dir)) * vSkyLightColor * lighting_factor;
		diffuse_light += saturate(dot(normal, sun_dir)) * vSunColor * lighting_factor;
		Out_Color = saturate(vMaterialColor * vColor * diffuse_light);
	}

	float4 In_Color = Out_Color;
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb *= float3(0.9, 1.1, 0.9);
	}
	else if ((season > 0.5) && (season < 1.5)) //1= summer
	{
		tex_col.rgb *= float3(1.0, 1.0, 1.0);
	}
	else if ((season > 1.5) && (season < 2.5)) //2= autumn
	{
		tex_col.rgb *= float3(1.1, 0.9, 0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}
	
	Output.RGBColor = In_Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_font(VS_OUTPUT_MAP_FONT In) 
{ 
	PS_OUTPUT Output;

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	Output.RGBColor =  In.Color * tex_col;

	//extra for fading out txt on map
	float dist = In.Map;
	dist = saturate(dist / 100.0);
	
	if(dist > 0.4) // if far away
	{
		float alphaval = dist - 0.15;
		alphaval *= 1.0 + alphaval;
		alphaval = min(alphaval, 0.85);
		Output.RGBColor.a *= saturate(alphaval); //makes visible
	}
	else
	{
		Output.RGBColor.a = 0.0;
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);

	if(/*ALPHA_TEST_ENABLED &&*/ (Output.RGBColor.a - (alpha_test_val * 1.25)) < 0.0)
	{
		discard;
	}

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_parallax_water(VS_OUTPUT_PARALLAX_WATER In, bool use_high, bool apply_depth, bool mud_factor)
{ 
	PS_OUTPUT Output;
	
	bool rgb_normalmap = false; //!apply_depth;
	
	In.Tex0 = In.Tex0 * 0.5;

	float Timer = GetTimer(1.0);

	float time_variable = 0.5 * time_var;//Timer;//
	float2 TexOffsetA = In.Tex0;
	float2 TexOffsetB = In.Tex0;

	float3 viewVec = normalize(In.ViewDir);

	float factor = (0.01 * vSpecularColor.x);
	float volume = (factor * 5.0);
	float bias = (factor * -2.5);

	TexOffsetA = float2(In.Tex0.x, In.Tex0.y + (0.1 * time_variable));
	float height = texture2D(MeshTextureSampler, TexOffsetA).a;
	float offset = height * volume + bias;
	
	TexOffsetB = float2(In.Tex0.x + (0.15 * time_variable),In.Tex0.y+ (0.25 * time_variable));
	float height2 = texture2D(SpecularTextureSampler, TexOffsetB).a;
	float offset2 = (height2) * (0.5 * volume) + (0.5 * bias);
	
	In.Tex0 += offset * viewVec.xy;
	In.Tex0 += offset2 * viewVec.xy;

	float3 normal;
	float3 normal2;
	if(rgb_normalmap)
	{
		normal = (2.0 * texture2D(Diffuse2Sampler, In.Tex0).rgb - 1.0);
	}
	else
	{
		//Normalmap A
		TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1 * time_variable));
		normal.xy = (2.0 * texture2D(Diffuse2Sampler, TexOffsetA).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
		
		//Normalmap B
		TexOffsetB = float2(In.Tex0.x,In.Tex0.y+ (0.25 * time_variable));// + (0.15*time_variable)
		normal2.xy = (2.0 * texture2D(NormalTextureSampler, TexOffsetB).ag - 1.0);
		normal2.z = sqrt(1.0 - dot(normal2.xy, normal2.xy));
		
		normal = lerp (normal,normal2, 0.35);
	}
	
	if(!apply_depth)
	{
		normal = float3(0.0, 0.0, 1.0);
	}

	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		float2 ref_tc = (0.25 * normal.xy) + float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.5 - 0.5 * (In.PosWater.y / In.PosWater.w));
		tex = texture2D(ReflectionTextureSampler, float2(ref_tc.x, 1.0 - ref_tc.y));
	}
	else
	{
		//for objects use env map (they use same texture register)
		float2 ref_tc = (vView - normal).yx * 3.4;
		tex = texture2D(EnvTextureSampler, float2(ref_tc.x, 1.0 - ref_tc.y));
	}
	
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01 * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125;
	}
	
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel* fresnel * fresnel * fresnel * fresnel);
	
	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01);
	}
	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160) * fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}

	Output.RGBColor.a = 1.0 - 0.3 * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0;
	}

	float3 g_cDownWaterColor = mud_factor ? float3(4.5 / 255.0, 8.0 / 255.0, 6.0 / 255.0) : float3(1.0 / 255.0, 4.0 / 255.0, 6.0 / 255.0);
	float3 g_cUpWaterColor   = mud_factor ? float3(5.0 / 255.0, 7.0 / 255.0, 7.0 / 255.0) : float3(1.0 / 255.0, 5.0 / 255.0, 10.0 / 255.0);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;

	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1;
		fog_fresnel_factor += 0.05;
	}

	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022, 0.02, 0.005) * (1.0 - saturate(dot(vView, normal)));
	}
	
	if(apply_depth && use_depth_effects)
	{	
		float2 proj_uv = In.projCoord.xy / In.projCoord.w;
		float depth = texture2D(DepthTextureSampler, float2(proj_uv.x, 1.0 - proj_uv.y)).r;
	
		float alpha_factor;
		if((depth + 0.0005) < In.Depth)
		{
			alpha_factor = 1.0;
		}
		else
		{
			alpha_factor = saturate(/*max(0, */(depth - In.Depth) * 2048.0);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth) * 32.0);
		

		// TODO_MKORKMAZ: fix refraction
		const bool use_refraction = false;
		
		if(use_refraction && use_high)
		{
			float4 coord_start = In.projCoord; //float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.45 + 0.5 * (In.PosWater.y / In.PosWater.w));
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1);
			float depth_here = texture2D(DepthTextureSampler, coord_disto.xy).r;
			float4 refraction;
			if(depth_here < depth)
				refraction = texture2DProj(ScreenTextureSampler, coord_disto);
			else
				refraction = texture2DProj(ScreenTextureSampler, coord_start);

			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, /*0.145 * fog_fresnel_factor*/ saturate(1.0 - Output.RGBColor.w) * 0.55);
			if(Output.RGBColor.a > 0.1)
			{
				Output.RGBColor.a *= 1.75;
			}
			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25;
			}
		}
	}
			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0;
	}
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}	

PS_OUTPUT ps_parallax_water2(VS_OUTPUT_PARALLAX_WATER In, bool use_high, bool apply_depth, bool mud_factor)
{ 
	PS_OUTPUT Output;
	
	bool rgb_normalmap = false; //!apply_depth;
	
	In.Tex0 = In.Tex0 * 0.5;

	float time_variable = 0.5 * time_var;
	float2 TexOffsetA = In.Tex0;
	float2 TexOffsetB = In.Tex0;

	float3 viewVec = normalize(In.ViewDir);
	{
     float factor = (0.01 * vSpecularColor.x);
     float bias = (factor * -2.5);//-0.02; 
     float volume = (factor * 5.0);//0.04;

	//PARALLAX TEX A
	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
	float height = texture2D(MeshTextureSampler, TexOffsetA).a;
	//height *= sin(0.5*time_variable + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//PARALLAX TEX B
	TexOffsetB = float2(In.Tex0.x + (0.15*time_variable),In.Tex0.y+ (0.25*time_variable));
	float height2 = texture2D(SpecularTextureSampler, TexOffsetB).a;
	float offset2 = (height2) * (0.5*volume) + (0.5*bias);
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0 += offset * viewVec.xy;
	In.Tex0 += offset2 * viewVec.xy;
	}

	float3 normal;
	float3 normal2;

	if(rgb_normalmap)
	{
		normal = (2.0 * texture2D(Diffuse2Sampler, In.Tex0).rgb - 1.0);
	}
	else
	{   //Normalmap A
		TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
		normal.xy = (2.0 * texture2D(Diffuse2Sampler, TexOffsetA).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
		
		//Normalmap b
		TexOffsetB = float2(In.Tex0.x,In.Tex0.y+ (0.25*time_variable));// + (0.15*time_variable)
		normal2.xy = (2.0 * texture2D(NormalTextureSampler, TexOffsetB).ag - 1.0);
		normal2.z = sqrt(1.0 - dot(normal2.xy, normal2.xy));
		
		normal = lerp (normal,normal2,0.35);
	}
	
	if(!apply_depth)
	{
		normal = float3(0,0,1);
	}
	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		float2 ref_tc = (0.25 * normal.xy) + float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.5 - 0.5 * (In.PosWater.y / In.PosWater.w));
		tex = texture2D(ReflectionTextureSampler, float2(ref_tc.x, 1.0 - ref_tc.y));
	}
	else
	{
		//for objects use env map (they use same texture register)
		tex = texture2D(EnvTextureSampler, (vView - normal).yx * 3.4);
	}
	
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01 * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125;
	}
	
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel* fresnel * fresnel * fresnel * fresnel);
	
	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01);
	}
	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160)*fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}
	Output.RGBColor.a = 1.0 - 0.3 * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0;
	}
	
	float3 g_cDownWaterColor = mud_factor ? float3(4.5/255.0, 8.0/255.0, 6.0/255.0) : float3(1.0/255.0, 4.0/255.0, 6.0/255.0);
	float3 g_cUpWaterColor   = mud_factor ? float3(5.0/255.0, 7.0/255.0, 7.0/255.0) : float3(1.0/255.0, 5.0/255.0, 10.0/255.0);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1;
		fog_fresnel_factor += 0.05;
	}
	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022, 0.02, 0.005) * (1.0 - saturate(dot(vView, normal)));
	}

	// TODO_MKORKMAZ: temporarily disabled
	if(false)
	//if(apply_depth && use_depth_effects)
	{	
		float depth = texture2DProj(DepthTextureSampler, In.projCoord).r;
	
		float alpha_factor;

		if((depth + 0.0005) < In.Depth)
		{
			alpha_factor = 1.0;
		}
		else
		{
			alpha_factor = saturate(/*max(0, */(depth - In.Depth) * 2048.0);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth) * 32.0);
		
		bool use_refraction = true;
		
		if(use_refraction && use_high)
		{
			float4 coord_start = In.projCoord; //float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.45 + 0.5 * (In.PosWater.y / In.PosWater.w));
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1);
			float depth_here = texture2D(DepthTextureSampler, coord_disto.xy).r;
			float4 refraction;
			if(depth_here < depth)
				refraction = texture2DProj(ScreenTextureSampler, coord_disto);
			else
				refraction = texture2DProj(ScreenTextureSampler, coord_start);

			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, /*0.145 * fog_fresnel_factor*/ saturate(1.0 - Output.RGBColor.w) * 0.55);
			if(Output.RGBColor.a > 0.1)
			{
				Output.RGBColor.a *= 1.75;
			}
			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25;
			}
		}
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0;
	}
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_icon_seasonal(VS_OUTPUT_ICON_SEASONAL In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(Diffuse2Sampler, In.Tex0.xy);
	if((tex_col.a - 0.5) < 0.0)
		discard;

	INPUT_TEX_GAMMA(tex_col.rgb);
	float4 tex_col_snow = texture2D(MeshTextureSampler, In.Tex0.xy);
	float snow_amount = texture2D(SpecularTextureSampler, In.Tex0.xy).a;

	float season = GetSeason();
	float height = In.Tex0.z;
	if (season > 2.5) //3= winter
	{
		height *= 2.0;
		height += 1.0;
	}
	else
	{
		height *= 1.0;
	}
	
	snow_amount = saturate(height * (snow_amount) - 1.5);
	float snow_present = texture2D(NormalTextureSampler, In.Tex0.xy).r;
	snow_amount *= snow_present;
	tex_col = lerp(tex_col,tex_col_snow,snow_amount);
	
	float sun_amount = 1.0; 
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_sea_foam(VS_OUTPUT_SEA_FOAM In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);

	float sun_amount = 1.0; 
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	Output.RGBColor =  tex_col * saturate(In.Color + In.SunLight * sun_amount);
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_bump_season(VS_OUTPUT_BUMP In, int PcfMode)
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;
	
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);

	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}

	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb *= float3(0.9, 1.1, 0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col.rgb *= float3(1.0, 1.0, 1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col.rgb *= float3(1.1, 0.9, 0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}	
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	float fresnel = 1.0 - (saturate(dot(In.ViewDir, In.WorldNormal)));

	Output.RGBColor.rgb *= max(0.6, fresnel*fresnel + 0.1); 	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_bump_bark(VS_OUTPUT_BUMP In, int PcfMode)
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;
	
	float3 normal = 0.25 * (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);

	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	float fresnel = 1.0 - (saturate(dot( In.ViewDir, In.WorldNormal)));

	Output.RGBColor.rgb *= max(0.6,fresnel*fresnel+0.1); 
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);

	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_parallax(VS_OUTPUT_PARALLAX In, int PcfMode)
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;

	float2 viewpara = In.ViewDir.xy;

    float factor = (0.01 * 6.3);//vSpecularColor.x);
    float BIAS = (factor * -0.5);//-0.02; 
    float SCALE = factor;//0.04;
    
    // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
    float4 Normal = texture2D(SpecularTextureSampler, In.Tex0);
    float h = Normal.a * SCALE + BIAS;
    In.Tex0.xy += h * Normal.z * viewpara;

	float3 normal;

	//normalmap type
	float rgb_or_green = texture2D(NormalTextureSampler, float2(0.5, 0.5)).r;
	if (rgb_or_green > 0.005)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	}
	else
	{
		normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	}


	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;

	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	float3 vView = normalize(In.ViewDir);
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	total_light.rgb += 0.5 * (total_light.rgb * fresnel); 
	total_light = saturate(total_light);
		
	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);

	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb *= float3(0.9, 1.1, 0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col.rgb *= float3(1.1, 0.9, 0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		float greyscale = dot(tex_col.rgb, float3(0.3, 0.59, 0.11));
		tex_col.rgb = lerp(float3(greyscale), tex_col.rgb, float3(0.75));
		float h = pow(texture2D(SpecularTextureSampler, In.Tex0).a, 2.0);
		h = saturate(h + 0.5);
		h = 1.0;
		float3 snow = texture2D(EnvTextureSampler, In.Tex0).rgb;
		tex_col.rgb = lerp(tex_col.rgb,snow,h);
	}

	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	if ((season < 2.5)) //  not winter (3= winter)
	{
		//parallax height darkening
		float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
		
		
		float h = texture2D(SpecularTextureSampler, In.Tex0).a;
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb * 0.75, Output.RGBColor.rgb * 1.2, h);
	}
	else
	{
		float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
		float3 outcolour = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35 + fresnel)),light_intenisty);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	outcolour, 0.5);
		
		float h = texture2D(SpecularTextureSampler, In.Tex0).a;
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, Output.RGBColor.rgb * 1.2,h);
	}

	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_parallax_multitex(VS_OUTPUT_PARALLAX In, int PcfMode)
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
	
	float2 viewpara = In.ViewDir.xy;
    float factor = (0.01 * 6.3);//vSpecularColor.x);
    float BIAS = (factor * -0.5);//-0.02; 
    float SCALE = factor;//0.04;
    
    // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
    float4 Normal = texture2D(SpecularTextureSampler, In.Tex0);
    float h = Normal.a * SCALE + BIAS;
    In.Tex0.xy += h * Normal.z * viewpara;

	float3 normal;
	//normalmap type
	float rgb_or_green = texture2D(NormalTextureSampler, float2(0.5, 0.5)).r;
	if (rgb_or_green > 0.005)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	}
	else
	{
		normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0).ag - 1.0);
		normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	}

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	float4 tex_col2 = texture2D(Diffuse2Sampler, In.Tex0 * uv_2_scale);
	
	float4 multi_tex_col = tex_col;
	float inv_alpha = (1.0 - In.VertexColor.a);
	multi_tex_col.rgb *= inv_alpha;
	multi_tex_col.rgb += tex_col2.rgb * In.VertexColor.a;
	
	INPUT_TEX_GAMMA(multi_tex_col.rgb);

	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	multi_tex_col.rgb *= float3(0.9, 1.1, 0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	multi_tex_col.rgb *= float3(1.0, 1.0, 1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	multi_tex_col.rgb *= float3(1.1, 0.9, 0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		float greyscale = dot(multi_tex_col.rgb, float3(0.3, 0.59, 0.11));
		multi_tex_col.rgb = lerp(float3(greyscale), multi_tex_col.rgb, 0.75);

		float h = texture2D(SpecularTextureSampler, In.Tex0 * 0.5).a;
		h *= texture2D(SpecularTextureSampler, In.Tex0).a;
		h += 0.5;
		h = 1.0;
		float3 snow = texture2D(EnvTextureSampler, In.Tex0).rgb;
		multi_tex_col.rgb = lerp(multi_tex_col.rgb,snow,saturate(h));
	}
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount)) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	//fresnel
	float3 vView = normalize(In.ViewDir);
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel* fresnel * fresnel);
	total_light.rgb += 0.5 * (total_light.rgb * fresnel); 
	total_light = saturate(total_light);
	
	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0;
	
	Output.RGBColor *= multi_tex_col;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	Output.RGBColor.a *= In.PointLightDir.a;
	
	if ((season < 2.5)) //  not winter (3= winter)
	{
		//parallax height darkening
		float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
		
		
		float h = texture2D(SpecularTextureSampler, In.Tex0).a;
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb * 0.75, Output.RGBColor.rgb * 1.2,h);
	}
	else
	{
		float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
		float3 outcolour = lerp(Output.RGBColor.rgb, (Output.RGBColor.rgb * (0.35 + fresnel)),light_intenisty);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	outcolour, 0.5);
		
		float h = texture2D(SpecularTextureSampler, In.Tex0).a;
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb * 1.2,h);
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_main_standart_sails(VS_OUTPUT_STANDART In, int PcfMode, bool use_bumpmap, bool use_specularfactor, bool use_specularmap, bool ps2x, bool use_aniso, bool terrain_color_ambient)
{ 
	PS_OUTPUT Output;

	float3 normal;
	if(use_bumpmap)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
		
	//define ambient term:
	int ambientTermType = ( terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0, 0.0, 1.0);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	float3 aniso_specular = float3(0.0);
	if(use_aniso)
	{
		if(!ps2x)
		{
			//GIVE_ERROR_HERE;
		}
		float3 direction = float3(0.0, 1.0 ,0.0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir.xyz : -vSunDir.xyz), In.ViewDir.xyz, In.Tex0);
	}
		
	if(use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.xyz;
	
		if(ps2x || !use_specularfactor) {
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
		{
			total_light.rgb += In.VertexLighting;
		}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[iLightIndices[0]]  * light_atten);
		#endif
	}
	else
	{
		total_light.rgb += (saturate(dot(-vSunDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.xyz;
		
		if(ambientTermType != 1 && !ps2x)
		{
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
		#endif
	}

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0);
		
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor)
	{
		float4 fSpecular = float4(0.0);
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		if(use_specularmap)
		{
			float spec_tex_factor = dot(texture2D(SpecularTextureSampler, In.Tex0).rgb, float3(0.33));	//get more precision from specularmap
			specColor *= spec_tex_factor;
		}
		else
		{
			specColor *= tex_col.a;
		}
		
		float4 sun_specColor = specColor * vSunColor * sun_amount;
		
		//sun specular
		float3 vHalf = normalize(In.ViewDir.xyz + ((use_bumpmap) ?  In.SunLightDir.xyz : -vSunDir.xyz));
		fSpecular = sun_specColor * pow(saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor.rgb * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE))
			{
				#ifndef USE_LIGHTING_PASS 
				//effective point light specular
				float light_atten = In.PointLightDir.a;
				float4 light_specColor = specColor * vLightDiffuse[iLightIndices[0]] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
				vHalf = normalize(In.ViewDir.xyz + In.PointLightDir.xyz);
				fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor.rgb * In.SkyLightDir.xyz * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	else if(use_specularmap)
	{
		//GIVE_ERROR_HERE; 
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	
	Output.RGBColor.r = 0.9;
	Output.RGBColor.gb = float2(0.2);
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = 1.0 ; //In.VertexColor.a;	//we dont control bUseMotionBlur to fit in 64 instruction
	
	if( (!use_specularfactor) || use_specularmap)
	{
		Output.RGBColor.a *= tex_col.a;
	}
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_main_standart_fresnel(VS_OUTPUT_STANDART In, int PcfMode, bool use_bumpmap, bool use_specularfactor, bool use_specularmap, bool ps2x, bool use_aniso, bool terrain_color_ambient)
{ 
	PS_OUTPUT Output;

	float3 normal;
	if(use_bumpmap)
	{
		normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0).rgb - 1.0);
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1.0;
	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
		
	//define ambient term:
	int ambientTermType = ( terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0, 0.0, 1.0);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	float3 aniso_specular = float3(0.0);
	if(use_aniso)
	{
		if(!ps2x)
		{
			//GIVE_ERROR_HERE;
		}

		float3 direction = float3(0.0, 1.0, 0.0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir.xyz : -vSunDir.xyz), In.ViewDir.xyz, In.Tex0);
	}
		
	if(use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.rgb;
	
		if(ps2x || !use_specularfactor)
		{
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}

		#ifdef INCLUDE_VERTEX_LIGHTING
		if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
		{
			total_light.rgb += In.VertexLighting.rgb;
		}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[iLightIndices[0]]  * light_atten);
		#endif
	}
	else
	{
		total_light.rgb += (saturate(dot(-vSunDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor.rgb;
		
		if(ambientTermType != 1 && !ps2x)
		{
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
		#endif
	}
	
	float3 vView = normalize(In.ViewDir);
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel* fresnel * fresnel * fresnel);
	fresnel *= 4.0;
	total_light.rgb += total_light.rgb * fresnel; 
	fresnel = pow(fresnel, 2.0);
	total_light.rgb += 0.020 * (total_light.rgb * fresnel); 

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0);
		
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor)
	{
		float4 fSpecular = float4(0.0);
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		if(use_specularmap)
		{
			float spec_tex_factor = dot(texture2D(SpecularTextureSampler, In.Tex0).rgb, float3(0.33));	//get more precision from specularmap
			specColor *= spec_tex_factor;
		}
		else
		{
			specColor *= tex_col.a;
		}
		
		float4 sun_specColor = specColor * vSunColor * sun_amount;
		
		//sun specular
		float3 vHalf = normalize(In.ViewDir.xyz + ((use_bumpmap) ?  In.SunLightDir.xyz : -vSunDir.xyz) );
		fSpecular = sun_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor.rgb * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE))
			{
			
				#ifndef USE_LIGHTING_PASS 
				//effective point light specular
				float light_atten = In.PointLightDir.a;
				float4 light_specColor = specColor * vLightDiffuse[iLightIndices[0]] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
				vHalf = normalize(In.ViewDir.xyz + In.PointLightDir.xyz);
				fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor.rgb * In.SkyLightDir.xyz * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	else if(use_specularmap)
	{
		//GIVE_ERROR_HERE; 
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = In.VertexColor.a;	//we dont control bUseMotionBlur to fit in 64 instruction
	
	if( (!use_specularfactor) || use_specularmap)
	{
		Output.RGBColor.a *= tex_col.a;
	}
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_flora_season_no_shadow(VS_OUTPUT_FLORA_SEASON_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	if (season < 0.5) //0= spring
	{
		tex_col = texture2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col = texture2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col = texture2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}

	/*if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;*/
	
	if((tex_col.a - 0.25) < 0.0)
		discard;
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_flora_season(VS_OUTPUT_FLORA_SEASON In, int PcfMode) 
{
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);

	if((tex_col.a - 0.5) < 0.0)
		discard;

	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col = texture2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col = texture2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col = texture2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor = tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = tex_col * ((In.Color + In.SunLight));
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_flora_season_grass(VS_OUTPUT_FLORA_SEASON In, int PcfMode) 
{ 
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col = texture2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col = texture2D(EnvTextureSampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col = texture2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}
	
	if((tex_col.a - 0.15) < 0.0)
		discard;
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;
	
	return Output;
}

PS_OUTPUT ps_flora_season_grass_no_shadow(VS_OUTPUT_FLORA_SEASON_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	if (season < 0.5) //0= spring
	{
	tex_col = texture2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5) && (season < 1.5)) //1= summer
	{
	tex_col = texture2D(EnvTextureSampler, In.Tex0);
	}
	else if ((season > 1.5) && (season < 2.5)) //2= autumn
	{
	tex_col = texture2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = texture2D(SpecularTextureSampler, In.Tex0);
	}
		
	if((tex_col.a - 0.15) < 0.0)
		discard;

	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;
	
	return Output;
}

PS_OUTPUT ps_flora_map(VS_OUTPUT_FLORA_MAP In, int PcfMode) 
{ 
	PS_OUTPUT Output;
	
	float2 TexCoord = In.Tex0.xy;
	float4 wave_amp = texture2D(SpecularTextureSampler, In.Tex0.xy);
	wave_amp.r = saturate(wave_amp.r * 0.01); //0.0 to 0.
		
	TexCoord.x += wave_amp.r * sin(10.9 * TexCoord.y + 0.7 * time_var); // NO.1= HEIGHT OF WAVE       NO.2= NUMBER OF WAVES    NO.3= SPEED OF WAVES
	
	float4 tex_col = texture2D(MeshTextureSampler, TexCoord);
	if((tex_col.a - 0.9) < 0.0)
		discard;

	float4 tex_col_snow = texture2D(Diffuse2Sampler, TexCoord);
	float snow_amount = 1.0;
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	float season = GetSeason();
	float height = In.Tex0.z;

	if (season > 2.5) //3= winter
	{	
		height *= 2.0;
		height -= 0.7;
	}
	else
	{
		height *= 0.1;
	}
	
	snow_amount = saturate(height * (snow_amount) - 1.5);
	tex_col = lerp(tex_col,tex_col_snow,snow_amount);

	if(ALPHA_TEST_ENABLED && (Output.RGBColor.a - alpha_test_val) < 0.0)
		discard;

	if (PcfMode != PCF_NONE)
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_new_map(VS_OUTPUT_NEW_MAP In, int PcfMode)
{
	PS_OUTPUT Output;
	
	float2 parallaxcoords = 0.95 * In.Tex0.xy;
	parallaxcoords.x = parallaxcoords.x + 0.1 * sin(parallaxcoords.y);
	
	float3 viewVec = normalize(In.CameraDir);
	float factor = (0.01 * vSpecularColor.x);
	float volume = (factor * 1.0);//0.04;
	float bias = (factor * -0.5);//-0.02; 

	float height = texture2D(EnvTextureSampler, parallaxcoords).a;
	float offset = height * volume + bias;
	
	In.Tex0.xy += offset * viewVec.xy;
	parallaxcoords += offset * viewVec.xy;
		
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	height = In.Tex0.z;
	if (season > 2.5) //3= winter
	{
		height *= 2.0;
		height += 1.65;
	}
	else
	{
		height *= 1.0;
	}
	
	tex_col.rgb += saturate(height * (tex_col.a) - 1.5);
	tex_col.a = 1.0;
	
	tex_col.rgb = lerp(tex_col.rgb * float3(0.8, 0.75, 0.65), tex_col.rgb * 1.30, 1.0 - texture2D(EnvTextureSampler, parallaxcoords).a);
	
	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0.xy * map_normal_detail_factor).rgb - 1.0);
	float3 normalpara = (2.0 * texture2D(EnvTextureSampler, parallaxcoords).rgb - 1.0);
	
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir.rgb)) * vec4(vSunColor.rgb, 1.0) * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1.0;
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	
	Output.RGBColor = tex_col * ((In.Color + In_SunLight * sun_amount));
	Output.RGBColor.a = In.Color.a;
	
	//add fresnel term
	{
		float fresnel = 1.0 - (saturate(dot( normalize(In.ViewDir), normalpara)));
		float fresnel2 = 1.0 - (saturate(dot( normalize(In.ViewDir), normal)));
		
		fresnel *= fresnel2; 
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*fresnel, 0.5);//max(0.6,fresnel+0.1); 
	}

	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_new_map_2(VS_OUTPUT_NEW_MAP In, int PcfMode)
{
	PS_OUTPUT Output;
		
	float2 parallaxcoords = 0.95 * In.Tex0.xy;
	parallaxcoords.x = parallaxcoords.x + 0.1 * sin(parallaxcoords.y);
	
	float3 viewVec = normalize(In.CameraDir);
	float factor = (0.01 * vSpecularColor.x);
	float volume = (factor * 1.0);//0.04;
	float bias = (factor * -0.5);//-0.02; 

	float height = texture2D(EnvTextureSampler, parallaxcoords).a;
	float offset = height * volume + bias;

	In.Tex0.xy += offset * viewVec.xy;
	parallaxcoords += offset * viewVec.xy;
	
	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	height = In.Tex0.z;
	float latitude = In.Tex0.w + 155.0; //(so origin is in mid north sea)

	if (season > 2.5) //3= winter
	{
		height *= 2.0;
		height += 1.0;
		height *= 1.5;
	}
	else
	{
		height *= 2.0;
		height += 1.0;
		latitude = 1.0 - saturate(latitude);
		latitude += 0.5;
		height *= latitude;
	}
	
	tex_col.rgb += saturate(height * (tex_col.a) - 1.5);
	tex_col.a = 1.0;
	
	//parallax darkening
	tex_col.rgb = lerp(tex_col.rgb*float3(0.8, 0.75, 0.65), tex_col.rgb * 1.30, 1.0 - texture2D(EnvTextureSampler, parallaxcoords).a);

	float3 normal = (2.0 * texture2D(NormalTextureSampler, In.Tex0.xy * map_normal_detail_factor).rgb - 1.0);
	float3 normalpara = (2.0 * texture2D(EnvTextureSampler, parallaxcoords).rgb - 1.0);
	
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1.0;
	if ((PcfMode != PCF_NONE))
	{
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		#else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord);
		#endif
	}
	
	Output.RGBColor = tex_col * ((In.Color + In_SunLight * sun_amount));
	Output.RGBColor.a = In.Color.a;
	
	float fresnel = 1.0 - (saturate(dot( normalize(In.ViewDir), normalpara)));
	float fresnel2 = 1.0 - (saturate(dot( normalize(In.ViewDir), normal)));

	fresnel *= fresnel2; 
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*fresnel, 0.5);//max(0.6,fresnel+0.1); 

	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_foam(bool reflections, VS_OUTPUT_MAP_WATER In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;

	float3 WorldPosition = In.PosWater.xyz;
	if ((WorldPosition.x < -125.0))
	{
		In.Tex0 *= 0.75;
		In.Tex0 = rotatevector(In.Tex0.xy, 225.0);
		In.Tex0.y -= (0.05 * time_var);
	}
	
	else if ((WorldPosition.y > 273.0) && (WorldPosition.x < -75.0))
	{
		In.Tex0 *= 0.75;
		In.Tex0 = 1.0 - In.Tex0;
		In.Tex0.y -= (0.05 * time_var);
	}
	else if ((WorldPosition.y > 213.0) && (WorldPosition.x > -75.0))
	{
		In.Tex0 *= 0.75;
		In.Tex0.y -= (0.05 * time_var);
	}
	else if ((WorldPosition.x > -125.0) && (WorldPosition.x < -50.0))
	{
		In.Tex0 *= 0.75;
		In.Tex0 = rotatevector(In.Tex0.xy, 90.0);
		In.Tex0.y -= (0.05 * time_var);
	}
	else if ((WorldPosition.y < 213.0) && (WorldPosition.x > -50.0))
	{
		In.Tex0 *= 0.75;
		In.Tex0 = rotatevector(In.Tex0.xy, 270.0);
		In.Tex0.y -= (0.05 * time_var);
	}
	else
	{
		In.Tex0.y -= (0.05 * time_var);
	}

	float4 tex_col = texture2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float3 normal;
	normal.xy = (2.0 * texture2D(NormalTextureSampler, In.Tex0 * 8.0).ag - 1.0);
	normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	
	float NdotL = saturate( dot(normal, In.LightDir) );
	float3 vView = normalize(In.CameraDir);

	// Fresnel term
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	Output.RGBColor.rgb += fresnel * In.Color.rgb;

	Output.RGBColor.rgb *= tex_col.rgb;

    Output.RGBColor.rgb *= 0.8;
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	Output.RGBColor.a = In.Color.a * tex_col.a;
	
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);
	
	return Output;
}

PS_OUTPUT ps_map_water_new(bool reflections, VS_OUTPUT_MAP_WATER_NEW In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor = 0.25 * In.Color;

	In.Tex0 *= 1.5;
	
	float time_variable = 0.2 * time_var;
	float2 TexOffsetA = In.Tex0;
	float2 TexOffsetB = In.Tex0;
	
	float3 viewVec = normalize(In.CameraDir);
	float factor = (0.01 * vSpecularColor.x);
	float volume = (factor * 1.4);//0.04;
	float bias = (factor * -0.7);//-0.02; 

	TexOffsetA = float2(In.Tex0.x + (0.25 * time_variable),In.Tex0.y );
	float height = texture2D(Diffuse2Sampler, TexOffsetA).a;
	float offset = height * volume + bias;

	TexOffsetB = float2(In.Tex0.x,In.Tex0.y + (0.15 * time_variable));
	float heightB = texture2D(Diffuse2Sampler, TexOffsetB).a;
	float offsetB = heightB * volume + bias;

	In.Tex0 += offset * (viewVec.xy);
	In.Tex0 += offsetB * (viewVec.xy);

	float3 normal;
	float3 normal2;
	TexOffsetA = float2(In.Tex0.x + (0.25 * time_variable),In.Tex0.y );
	normal.xy = (2.0 * texture2D(NormalTextureSampler, TexOffsetA).ag - 1.0);
	normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));

	TexOffsetB = float2(In.Tex0.x,In.Tex0.y + (0.15 * time_variable));
	normal2.xy = (2.0 * texture2D(NormalTextureSampler, TexOffsetB).ag - 1.0);
	normal2.z = sqrt(1.0 - dot(normal2.xy, normal2.xy));

	normal = lerp(normal,normal2, 0.5);
	
	float dist = In.Depth.y;
	dist = saturate(dist * 0.0075);
    
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));

	Output.RGBColor = 0.01 * NdotL * In.LightDif;
	
	float3 vView = normalize(In.CameraDir);
	float2 reflectcoords = (0.25 * normal.xy) + float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.5 - 0.5 * (In.PosWater.y / In.PosWater.w));
	float4 tex = texture2D(ReflectionTextureSampler, float2(reflectcoords.x, 1.0 - reflectcoords.y));
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	float3 RefColor = saturate((tex.rgb * fresnel));

	float coastheight = saturate((In.Color.w - 0.361) * 2.0);
		
	Output.RGBColor.a = 1.0 - 0.3 * In.CameraDir.z;
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	//Diffuse Colouring
	float3 cWaterColor = 5.0 * float3(1.0 / 255.0, 5.0 / 255.0, 10.0 / 255.0);
	
	float3 WaterColorLightDark = lerp(cWaterColor * 0.5, cWaterColor * 1.2, 1.0 - (texture2D(Diffuse2Sampler, TexOffsetA).a));//saturate(dot(vView, normal)));
	cWaterColor = lerp(WaterColorLightDark, cWaterColor, dist);//make ligth dark only when close
	
	float fresnel2 = 1.0 - saturate(dot(In.CameraDir.xyz, normal));
	fresnel2 *= max(0.25, In.Color.r);
	cWaterColor = cWaterColor * fresnel2;
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir.xyz, normal));
	float3 DifColor = cWaterColor;//(2*cWaterColor) * fresnel;
	
	if (In.CameraDir.z > 0.5)
	{
		Output.RGBColor.rgb += lerp((DifColor + RefColor), (12.0 * DifColor + 5.0 * RefColor), In.CameraDir.z - 0.5);
	}
	else
	{
		Output.RGBColor.rgb += (DifColor + RefColor);
	}

	//implement foam coords
    float2 FoamOffset = float2(2.0 * In.Tex0.x, 2.0 * In.Tex0.y - (0.1 * time_variable));

	float2 oceanfloorcord = In.Tex0;
	float3 viewVecOceanFloor = normalize(In.CameraDir);
	factor = (0.01 * vSpecularColor.x);
	volume = (factor * 20.0);
	bias = (factor * -10.0);

	height = 1.0 - (0.5 * coastheight);
	offset = height * volume + bias;
	
	In.Tex0.y *= 1.333;
	oceanfloorcord = In.Tex0 - offset * viewVecOceanFloor.xy;
	oceanfloorcord *= 2.0;
	
	if (coastheight > 0.08)
	{
		float3 oceanfloorstrong = 0.5 * (coastheight - 0.08) * (texture2D(SpecularTextureSampler,oceanfloorcord).rgb);
		float3 oceanfloorweak = 0.17 * (coastheight - 0.08) * (texture2D(SpecularTextureSampler,oceanfloorcord).rgb);
		oceanfloorstrong *= max(float3(0.25), In.Color.rgb);
		oceanfloorweak *= max(float3(0.25), In.Color.rgb);

		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb +oceanfloorstrong,Output.RGBColor.rgb +oceanfloorweak,saturate(dist * 1.8));
	
		//caustics
		float3 caustics = 0.5 * saturate((coastheight - 0.08) * (float3(0.0, 0.0, 0.0) + (texture2D(SpecularTextureSampler,(0.4 * oceanfloorcord) + 0.075 * time_var).a)));
		caustics += 0.5 * saturate((coastheight - 0.08)*(float3(0.0, 0.0, 0.0) + (texture2D(SpecularTextureSampler,float2((0.4 * oceanfloorcord.x) - 0.08 * time_var,(0.4 * oceanfloorcord.x) - 0.089*time_var)).a)));
		caustics *= 0.5;
		caustics *= float3 (0.2, 0.2, 1.0);
		caustics*= max(float3(0.25), In.Color.rgb);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb + 0.95 * caustics,Output.RGBColor.rgb + 0.25 * caustics,saturate(dist * 1.5));
		
		//foam
		float3 FoamColor = saturate(float3(0.0, 0.0, 0.0) + 0.4 * ((coastheight-0.08) * pow(texture2D(MeshTextureSampler, FoamOffset).a, 2.0)));
		FoamColor *= max(float3(0.25), In.Color.rgb);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb + 0.95 * FoamColor,Output.RGBColor.rgb + 0.10 * FoamColor,saturate(dist * 2.0));
	}

	Output.RGBColor.a = 1.0;			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}

PS_OUTPUT ps_map_water_river_new(bool reflections, VS_OUTPUT_MAP_WATER_NEW In) 
{ 
	PS_OUTPUT Output;
	In.Color *= 0.5;
	Output.RGBColor =  0.25 * In.Color;
	
	float time_variable = 0.2 * time_var;//Timer;//
	float2 TexOffsetA =In.Tex0;
	float2 TexOffsetB =In.Tex0;

	float3 viewVec = normalize(In.CameraDir);

	float factor = (0.01 * vSpecularColor.x);
	float volume = (factor * 1.0);//0.04;
	float bias = (factor * -0.5);//-0.02; 

	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1 * time_variable));
	float height = texture2D(Diffuse2Sampler, TexOffsetA).a;
	float offset = height * volume + bias;
	
	In.Tex0 += offset * viewVec.xy;

	float3 normal;
	float3 normal2;

	//Normalmap A
	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1 * time_variable));
	normal.xy = (2.0 * texture2D(NormalTextureSampler, TexOffsetA).ag - 1.0);
	normal.z = sqrt(1.0 - dot(normal.xy, normal.xy));
	
	//Lighting	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));

	Output.RGBColor = 0.01 * NdotL * In.LightDif;
	
	float3 vView = normalize(In.CameraDir);
	float2 reflectcoords = (0.25 * normal.xy) + float2(0.5 + 0.5 * (In.PosWater.x / In.PosWater.w), 0.5 - 0.5 * (In.PosWater.y / In.PosWater.w));
	float4 tex = texture2D(ReflectionTextureSampler, reflectcoords);
	INPUT_OUTPUT_GAMMA(tex.rgb);

	float fresnel = 1.0 - (saturate(dot(vView, normal)));
	fresnel = 0.0204 + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	float3 RefColor = saturate((0.5 * (tex.rgb * fresnel)));
		
    float3 coastproximity = saturate(min(pow(In.Color.rgb + float3(0.23), float3(2.3)), In.Color.rgb));
    RefColor *= saturate(float3(0.8) - coastproximity);
	
	Output.RGBColor.a = 1.0 - 0.3 * In.CameraDir.z;
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	//Diffuse Colouring
	float3 g_cDownWaterColor = lerp(float3(4.5 / 255.0, 8.0 / 255.0, 6.0 / 255.0),float3(1.0 / 255.0, 4.0 / 255.0, 6.0 / 255.0),(1.0 - In.Color.rgb));
	float3 g_cUpWaterColor   = lerp(float3(5.0 / 255.0, 7.0 / 255.0, 7.0 / 255.0),float3(1.0 / 255.0, 5.0 / 255.0, 10.0 / 255.0),(1.0 - In.Color.rgb));
	float3 cWaterColor = lerp(g_cUpWaterColor, g_cDownWaterColor, 1.0 - (texture2D(Diffuse2Sampler, TexOffsetA).a));

	float dist = In.Depth.y;
	dist = saturate(dist * 0.0075);
	cWaterColor = lerp(cWaterColor, g_cUpWaterColor, dist);//saturate(dot(vView, normal)));
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	cWaterColor *= 3.0;
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	float3 DifColor = cWaterColor * saturate(0.5 * fog_fresnel_factor);
	DifColor = (2.0 * cWaterColor) * fresnel;

    Output.RGBColor.rgb += lerp((DifColor + 0.65 * RefColor), (DifColor + 0.45 * RefColor), dist);

	//implement foam
    float2 FoamTexCo = float2((In.Tex0.x + 0.10 * sin(2.0 * In.Tex0.y)), (In.Tex0.y+ 0.10 * sin(2.4 * In.Tex0.y)));
	float2 FoamOffset = float2(In.Tex0.x, In.Tex0.y - (0.1 * time_variable));
	float foam = texture2D(MeshTextureSampler, FoamOffset).a;
	float3 FoamColor = lerp(Output.RGBColor.rgb, Output.RGBColor.rgb + float3(foam), saturate(pow(In.Color.rgb + float3(0.25), float3(2.0)))); //lerp so more foam near coasts (In.Color)
	Output.RGBColor.rgb = lerp(FoamColor, Output.RGBColor.rgb, min(dist, 0.85));//lerp so more foam less visible when far zoomed out

	float2 oceanfloorcord = In.Tex0;
	float3 viewVecOceanFloor = normalize(In.CameraDir.xyz);
	factor = (0.01 * vSpecularColor.x);
	volume = (factor * 15.0);//0.04;
	bias = (factor * -12.5);//-0.02; 

	height = 1.0;
	offset = height * volume + bias;
	
	In.Tex0.y *= 1.333;
	oceanfloorcord = In.Tex0 - offset * viewVecOceanFloor.xy;
	
	if (In.Color.r > 0.08)
	{
		Output.RGBColor.rgb += (In.Color.r - 0.08) * (texture2D(SpecularTextureSampler,oceanfloorcord)).rgb;
		//extra foam
		Output.RGBColor.rgb += 0.15 * ((In.Color.r - 0.08) * texture2D(MeshTextureSampler, FoamOffset).a);
	}
	
    Output.RGBColor.rgb = saturate(Output.RGBColor.rgb);
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, Output.RGBColor.rgb * In.LightDif.rgb, 0.75);

	Output.RGBColor.g *= 0.95;
	Output.RGBColor.a = 1.0;			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	Output.RGBColor.rgb = lerp(vFogColor.rgb, Output.RGBColor.rgb, In.Fog);

	return Output;
}
