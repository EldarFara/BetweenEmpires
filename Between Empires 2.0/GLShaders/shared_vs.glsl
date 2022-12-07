
uniform float4x4 matWorldViewProj;
uniform float4x4 matWorldView;
uniform float4x4 matWorld;
uniform float4x4 matWaterWorldViewProj;
#ifndef DISABLE_GPU_SKINNING
uniform float4x4 matWorldArray[NUM_WORLD_MATRICES];
#endif
uniform float4x4 matWaterViewProj;
uniform float4x4 matMotionBlur;
uniform float4x4 matSunViewProj;
uniform float4x4 matView;
uniform float4x4 matViewProj;
uniform float4 vLightPosDir[NUM_LIGHTS];
uniform float4 vCameraPos;
uniform float4 texture_offset;
uniform float4 vDepthRT_HalfPixel_ViewportSizeInv;
uniform float flora_detail;

#ifdef USE_ShadowTexelPos_INTERPOLATOR
uniform float fShadowMapSize;
#endif

float3x3 float3x3_transpose(vec3 v0, vec3 v1, vec3 v2)
{
	return float3x3(vec3(v0.x, v1.x, v2.x), 
					vec3(v0.y, v1.y, v2.y),
					vec3(v0.z, v1.z, v2.z));
}

#ifndef DISABLE_GPU_SKINNING
vec4 skinning_deform(vec4 vPosition, vec4 vBlendWeights, vec4 vBlendIndices)
{
	return 	  mul(matWorldArray[int(vBlendIndices.x)], vPosition) * vBlendWeights.x
			+ mul(matWorldArray[int(vBlendIndices.y)], vPosition) * vBlendWeights.y
			+ mul(matWorldArray[int(vBlendIndices.z)], vPosition) * vBlendWeights.z
			+ mul(matWorldArray[int(vBlendIndices.w)], vPosition) * vBlendWeights.w;
}
#endif

mat4 build_instance_frame_matrix(vec3 vInstanceData0, vec3 vInstanceData1, vec3 vInstanceData2, vec3 vInstanceData3) 
{
	vec3 position = vInstanceData0.xyz;
	
	vec3 frame_s = vInstanceData1;
	vec3 frame_f = vInstanceData2;
	vec3 frame_u = vInstanceData3;
	
	mat4 matWorldOfInstance  = mat4(	frame_s.x, frame_f.x, frame_u.x, position.x, 
										frame_s.y, frame_f.y, frame_u.y, position.y, 
										frame_s.z, frame_f.z, frame_u.z, position.z, 
										0.0, 0.0, 0.0, 1.0  );

	return matWorldOfInstance;
}

float4 calculate_point_lights_diffuse(float4 vWorldPos, float3 vWorldN, bool face_like_NdotL, bool exclude_0) 
{
	const int exclude_index = 0;
	
	float4 total = vec4(0.0);
	for(int j = 0; j < iLightPointCount; j++)
	{
		if(!exclude_0 || j != exclude_index)
		{
			int i = iLightIndices[j];
			float3 point_to_light = vLightPosDir[i].xyz - vWorldPos.xyz;
			float LD = dot(point_to_light, point_to_light);
			float3 L = normalize(point_to_light);
			float wNdotL = dot(vWorldN, L);
			
			float fAtten = VERTEX_LIGHTING_SCALER / LD;
			//compute diffuse color
			if(face_like_NdotL)
			{
				total += max(0.2 * (wNdotL + 0.9), wNdotL) * vLightDiffuse[i] * fAtten;
			}
			else
			{
				total += saturate(wNdotL) * vLightDiffuse[i] * fAtten;
			}
		}
	}
	return total;
}

float4 calculate_point_lights_specular(float3 vWorldPos, float3 vWorldN, float3 vWorldView, bool exclude_0)
{
	//const int exclude_index = 0;
	
	float4 total = vec4(0.0);
	for(int i = 0; i < iLightPointCount; i++)
	{
		//if(!exclude_0 || j != exclude_index)	//commenting varying exclude_0 will introduce double effect of light0, but prevents loop bug of fxc
		{
			//int i = iLightIndices[j];
			float3 point_to_light = vLightPosDir[i].xyz - vWorldPos;
			float LD = dot(point_to_light, point_to_light);
			float3 L = normalize(point_to_light);
					
			float fAtten = VERTEX_LIGHTING_SPECULAR_SCALER / LD;
				
			float3 vHalf = normalize( vWorldView + L );
			total += fAtten * vLightDiffuse[i] * pow( saturate(dot(vHalf, vWorldN)), fMaterialPower); 
		}
	}
	return total;
}

VS_OUTPUT_FONT vs_skybox(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FONT Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Pos.z = Out.Pos.w;

	float3 P = vPosition.xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;

	//apply fog
	P.z *= 0.2;
	float d = length(P);
	float4 vWorldPos = mul(matWorld, vPosition);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	Out.Color.a = (vWorldPos.z < -10.0) ? 0.0 : 1.0;
	
	return Out;
}


// AON wind animation for flora.
float3 CalcFloraVertexAnimation(float2 Offset)
{
    float vFloraWindStrength = 0.14;

	float displacementamp = 0.033 * -40.0; //applying user-specified amplitude
	float displacementfreq = 0.33 * 3.6; //applying user-specified frequency
	float displacementscale = 2.5 * (vFloraWindStrength * 0.129); //applying user-specified scale 0.014 + 4 = 0.018
  
	float grandwave = sin(time_var * 0.2);
  
	// float standardoffsetx = (vFloraWindStrength * 0.75f); // 0.1
	// float standardoffsety = (standardoffsetx * 0.5f); 
  
	float3 wind = float3(0.0, 0.0, 0.0);

	// create wind X/Y displacement coefficients using world-space vertex positions
	wind.x += sin (Offset.x * displacementamp + time_var * displacementfreq) * displacementscale;
	wind.y += cos (Offset.y * (displacementamp * 0.5) + time_var * displacementfreq) * (displacementscale * 0.5);
  
	wind *= grandwave;
  
	wind.x -= displacementscale;
	wind.z += (wind.x * 0.5);// * 0.8);
	wind.y -= (displacementscale * 0.5);
  
	return wind;
}

float3 CalcFloraPineVertexAnimation(float3 Offset)
{  
    float vFloraWindStrength = 0.14;

	float displacementamp = 0.033 * -40.0; //applying user-specified amplitude
	float displacementfreq = 0.33 * 3.6; //applying user-specified frequency
	float displacementscale = 2.5 * (vFloraWindStrength * 0.129); //applying user-specified scale 0.014 + 4 = 0.018
  
	float grandwave = sin(time_var * 0.2);
  
	// float standardoffsetx = (vFloraWindStrength * 0.75f); // 0.1
	// float standardoffsety = (standardoffsetx * 0.5f); 
  
	float3 wind = float3(0.0, 0.0, 0.0);

	// create wind X/Y displacement coefficients using world-space vertex positions
	wind.x += sin ((Offset.z-(Offset.x * 2.0)) * displacementamp + time_var * displacementfreq) * displacementscale;
	wind.y += cos (Offset.y * (displacementamp * 0.5) + time_var * displacementfreq) * (displacementscale * 0.5);
  
	wind *= grandwave;
  
	wind.x -= displacementscale;
	wind.z += (wind.x * 0.5);// * 0.8);
	wind.y -= (displacementscale * 0.5);
  
	// Offset.xyz += wind;
	return wind;//Offset.xyz;
}


VS_OUTPUT_FLORA vs_flora(int PcfMode, float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	Out.Tex0 = tc;
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor.bgra * (vAmbientColor + vec4(vSunColor.rgb, 1.0) * 0.06); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor.rgb * 0.15);
	//shadow mapping variables
	Out.SunLight = (vec4(vSunColor.rgb, 1.0) * 0.34)* vMaterialColor * vColor.bgra;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT vs_main(int PcfMode, bool UseSecondLight, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor.bgra;
	}

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT vs_main_Instanced(int PcfMode, bool UseSecondLight, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor,
						   float3 vInstanceData0, float3 vInstanceData1, float3 vInstanceData2, float3 vInstanceData3)
{
	VS_OUTPUT Out;

	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);
	
	//-- Out.Pos = mul(matWorldViewProj, vPosition);
    Out.Pos = mul(matWorldOfInstance, float4(vPosition.xyz, 1.0));
    Out.Pos = mul(matViewProj, Out.Pos);

	float4 vWorldPos = mul(matWorldOfInstance,vPosition);
	float3 vWorldN = normalize(mul(matWorldOfInstance, vec4(vNormal, 0.0)).xyz); //normal in world space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float4 P = mul(matView, vWorldPos); //position in view space
	float d = length(P.xyz);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


////////// Beaver Flag Shader
float CalcPennonAnimation(float3 Offset)
{ 
  float curtime = (time_var * 9.0);
  
  return float(sin(curtime+Offset.z+(Offset.y-Offset.x)) * (Offset.x * 0.33)); //sin(time_var+Offset.z+(Offset.y-Offset.x)) * 0.05
}

float CalcPennonVerticalAnimation(float3 Offset)
{ 
  float curtime = (time_var * 9.0);
  
  return float(sin(curtime+Offset.z+(Offset.z-Offset.x))); //sin(time_var+Offset.z+(Offset.y-Offset.x)) * 0.05
}

float CalcFlagAnimation(float3 Offset)
{   
  float curtime = (time_var * 4.0);
  
  return float(sin(curtime+Offset.z+(Offset.y-Offset.x)) * (Offset.x * 0.15)); //sin(time_var+Offset.z+(Offset.y-Offset.x)) * 0.05
}

float CalcCTFPennonAnimation(float3 Offset)
{   
  float curtime = (time_var * 8.0);
  
  return float(sin(curtime+Offset.z+(Offset.y-Offset.x)) * (Offset.y * 0.3)); //sin(time_var+Offset.z+(Offset.y-Offset.x)) * 0.05
}

float3 CalcSailAnimation(float3 Offset)
{   
	float vFloraWindStrength = 0.14;
    float grandwave = sin(time_var * 0.2);
    float curtime = (time_var * 2.5);
    float xmul = (Offset.x * (vFloraWindStrength * 0.08)); // 0.01
    float value = (sin(curtime+Offset.z+(Offset.y-Offset.x)) * xmul);
    value *= grandwave;
    return float3(value,value,value);
}

VS_OUTPUT_STANDART vs_main_standart(vec4 vPosition, vec2 tc, vec3 vNormal, vec4 vVertexColor, vec3 vTangent, vec3 vBinormal, vec4 vBlendWeights, vec4 vBlendIndices, int PcfMode,
	bool use_bumpmap, bool use_skinning, 
	int flagwave_type)
{	
	VS_OUTPUT_STANDART Out;

	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
#ifndef DISABLE_GPU_SKINNING
	if(use_skinning)
	{
		vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
		
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = normalize(  mul(matWorldArray[int(vBlendIndices.x)], vec4(vTangent, 0.0)).xyz * vBlendWeights.x
									+ mul(matWorldArray[int(vBlendIndices.y)], vec4(vTangent, 0.0)).xyz * vBlendWeights.y
									+ mul(matWorldArray[int(vBlendIndices.z)], vec4(vTangent, 0.0)).xyz * vBlendWeights.z
									+ mul(matWorldArray[int(vBlendIndices.w)], vec4(vTangent, 0.0)).xyz * vBlendWeights.w);
			
			vObjectB = /*normalize*/(cross(vObjectN, vObjectT));	
			bool left_handed = (dot(cross(vNormal, vTangent), vBinormal) < 0.0);

			if(left_handed)
			{
				vObjectB = -vObjectB;
			}
		}
	}
	else
#endif
	{
		if ( (flagwave_type > 0)
			&& (flagwave_type != 3 || ((tc.y >= 0.07 && tc.y <= 0.93) || ((tc.y <= 0.07 || tc.y >= 0.93) && (tc.x >= 0.07 && tc.x <= 0.93))))
			)
		{
			float4 orgPos = vPosition;
			float sideval = 0.0;
			float4 Position1;
			float4 Position2;
			float4 nextPos = orgPos;
			for(int p=1;p<3;p++)
			{
				if(p == 2)
				{
					nextPos.x = orgPos.x;
					nextPos.y -= 0.05;
				}
				else
					nextPos.x += 0.05;					

				if(p == 1)
				{
					Position1 = nextPos;
				}
				if(p == 2)
				{
					Position2 = nextPos;
				}
			}
			if (flagwave_type == 1)
			{
				sideval = vNormal.z;
				vPosition.z += CalcPennonAnimation(vPosition.xyz);
				Position1.z += CalcPennonAnimation(Position1.xyz);
				Position2.z += CalcPennonAnimation(Position2.xyz);
			}
			else if (flagwave_type == 2)
			{
				sideval = -vNormal.y;
				vPosition.y += CalcFlagAnimation(vPosition.xyz);
				Position1.y += CalcFlagAnimation(Position1.xyz);
				Position2.y += CalcFlagAnimation(Position2.xyz);
			}
			else if (flagwave_type == 3)
			{
				sideval = vNormal.z;
				vPosition.xyz += CalcSailAnimation(vPosition.xyz);
				Position1.xyz += CalcSailAnimation(Position1.xyz);
				Position2.xyz += CalcSailAnimation(Position2.xyz);
			}
			else if (flagwave_type == 4)
			{
				sideval = -vNormal.x;
				vPosition.x += CalcCTFPennonAnimation(vPosition.xyz);
				Position1.x += CalcCTFPennonAnimation(Position1.xyz);
				Position2.x += CalcCTFPennonAnimation(Position2.xyz);
			}
			else if (flagwave_type == 5)
			{
				//   sideval = vNormal.x;
				vPosition.x += (CalcPennonVerticalAnimation(vPosition.xyz) * (tc.x * 0.6));
				//   Position1.x += (CalcPennonVerticalAnimation(Position1.xyz) * (tc.x * 0.6));
				//   Position2.x += (CalcPennonVerticalAnimation(Position2.xyz) * (tc.x * 0.6));
			}

			// Calculate a new normal for the combined positions
			if (flagwave_type != 5)
			{
				vNormal = cross(Position1.xyz-vPosition.xyz,Position2.xyz-vPosition.xyz);
			}

			if (flagwave_type == 2)
			{
				vNormal.y += 1.0; // flags are rotated down so fix it with a simple float rotate up.
			}
			else if (flagwave_type == 4)
			{
				vNormal.x += 1.0; // flags are rotated down so fix it with a simple float rotate up.
			}

			// If the flag is opposite side then reverse normal
			if(sideval > 0.0) 
			{
				vNormal = -vNormal;
			}
		}

		vObjectPos = vPosition;
		
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = vTangent;
			vObjectB = vBinormal;
		}
	}
	
	float4 vWorldPos = mul(matWorld, vObjectPos);
	float3 vWorldN = normalize(mul(matWorld, vec4(vObjectN, 0.0)).xyz);	
	
	bool use_motion_blur = bUseMotionBlur && (!use_skinning);
	
	if(use_motion_blur)	//motion blur flag!?!
	{
		#ifdef STATIC_MOVEDIR //(used in instanced rendering )
			const float blur_len = 0.25;
			float3 moveDirection = -normalize( float3(matWorld[0][0],matWorld[1][0],matWorld[2][0]) );
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			float4 vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		#else 
			float4 vWorldPos1 = mul(matMotionBlur, vObjectPos);
			float3 moveDirection = normalize(vWorldPos1 - vWorldPos).xyz;
		#endif
		
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.1) ? 1.0 : 0.0;

		float y_factor = saturate(vObjectPos.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5);

		float extra_alpha = 0.1;
		float start_alpha = (1.0+extra_alpha);
		float end_alpha = start_alpha - 1.8;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vVertexColor.a = saturate(0.5 - vObjectPos.y) + alpha + 0.25;
	}

	if(use_motion_blur)
	{
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vObjectPos);
	}

	Out.Tex0 = tc;	
	
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul(matWorld, vec4(vObjectB, 0.0)).xyz);
		float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vObjectT, 0.0)).xyz);
		float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
		Out.SkyLightDir = mul(TBNMatrix, float3(0,0,1)); //STR_TEMP!?
		Out.VertexColor = vVertexColor.bgra;
		
		//point lights
		#ifdef INCLUDE_VERTEX_LIGHTING
			Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, true).xyz;
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			int effective_light_index = iLightIndices[0];
			float3 point_to_light = vLightPosDir[effective_light_index].xyz - vWorldPos.xyz;
			Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
			
			float LD = dot(point_to_light, point_to_light);
			Out.PointLightDir.a = saturate(1.0/LD);	//prevent bloom for 1 meters
		#endif
		
		float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.ViewDir =  mul(TBNMatrix, viewdir);
		
		#ifndef USE_LIGHTING_PASS
			if (PcfMode == PCF_NONE)
			{
				Out.ShadowTexCoord = calculate_point_lights_specular(vWorldPos.xyz, vWorldN, viewdir, true);
			}
		#endif
	}
	else
	{

		Out.VertexColor = vVertexColor.bgra;
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false).xyz;
		#endif
		
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
		
		Out.SunLightDir = vWorldN;
		#ifndef USE_LIGHTING_PASS
		Out.SkyLightDir = calculate_point_lights_specular(vWorldPos.xyz, vWorldN, Out.ViewDir, false).xyz;
		#endif
	}
	Out.VertexColor.a *= vMaterialColor.a;	

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vObjectPos).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
		
	return Out;
}

VS_OUTPUT_BUMP vs_main_bump(int PcfMode, float4 vPosition, float3 vNormal, float2 tc,  float3 vTangent, float3 vBinormal, float4 vVertexColor, float4 vPointLightDir)
{
	VS_OUTPUT_BUMP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	float4 vWorldPos = mul(matWorld, vPosition);
	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir.xyz);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	
	#ifdef USE_LIGHTING_PASS
		Out.PointLightDir = vWorldPos;
	#else
		Out.PointLightDir.rgb = 2.0 * vPointLightDir.rgb - 1.0;
		Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor.bgra;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); 

	Out.WorldNormal = vWorldN;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA vs_flora_Instanced(int PcfMode, float4 vPosition, float4 vColor, float2 tc,
								   //instance data:
								   float3   vInstanceData0,
								   float3   vInstanceData1,
								   float3   vInstanceData2,
								   float3   vInstanceData3)
{
	VS_OUTPUT_FLORA Out;
	
	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);

	float4 vWorldPos = mul(matWorldOfInstance, vPosition);
	Out.Pos = mul(matViewProj, vWorldPos);

	Out.Tex0 = tc;
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor.bgra * (vAmbientColor + vec4(vSunColor.rgb, 1.0) * 0.06); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor.rgb * 0.15);
	//shadow mapping variables
	Out.SunLight = (vec4(vSunColor.rgb, 1.0) * 0.34)* vMaterialColor * vColor.bgra;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matView, vWorldPos).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA_NO_SHADOW vs_flora_no_shadow(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_NO_SHADOW Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA vs_grass(int PcfMode, float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vAmbientColor;

	//shadow mapping variables
	if (PcfMode != PCF_NONE)
	{
		Out.SunLight = (vec4(vSunColor.rgb, 1.0) * 0.55) * vMaterialColor * vColor.bgra;
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
	}
	else
	{
		Out.SunLight = vec4(vSunColor.rgb, 1.0) * 0.5 * vColor.bgra;
	}
	//shadow mapping variables end
	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	Out.Color.a = min(1.0,(1.0 - (d / 50.0)) * 2.0);

	return Out;
}

VS_OUTPUT_FLORA_NO_SHADOW vs_grass_no_shadow(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_NO_SHADOW Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld,vPosition);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	Out.Color.a = min(1.0,(1.0 - (d / 50.0)) * 2.0);

	return Out;
}

VS_OUTPUT_FLORA vs_flora_billboards(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_FLORA Out;

	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	float dist_to_vertex = length(view_vec);

	/*if(dist_to_vertex < flora_detail_clip)
	{
		Out.Pos = float4(0.0, 0.0, -2.0, 1.0);
		return Out;
	}*/
	
	float alpha_val = saturate(0.5 + ((dist_to_vertex - flora_detail_fade) / flora_detail_fade_inv));	 
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space	

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	
	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);
	Out.Color.a *= alpha_val;

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_BUMP vs_main_bump_billboards(int PcfMode, float4 vPosition, float3 vNormal, float2 tc,  float3 vTangent, float3 vBinormal, float4 vVertexColor, float4 vPointLightDir)
{
	VS_OUTPUT_BUMP Out;

	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	float dist_to_vertex = length(view_vec);

	/*if(dist_to_vertex < flora_detail_clip)
	{
		Out.Pos = float4(0.0, 0.0, -2.0, 1.0);
		return Out;
	}*/

	float alpha_val = saturate(0.5 + ((dist_to_vertex - flora_detail_fade) / flora_detail_fade_inv));

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir.xyz);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	
	#ifdef USE_LIGHTING_PASS
		Out.PointLightDir = vWorldPos;
	#else
		Out.PointLightDir.rgb = 2.0 * vPointLightDir.rgb - 1.0;
		Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor.bgra;
	Out.VertexColor.a *= alpha_val;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	Out.WorldNormal = vWorldN;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_ENVMAP_SPECULAR vs_envmap_specular(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_ENVMAP_SPECULAR Out;

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	
	if(bUseMotionBlur)	//motion blur flag!?!
	{
		float4 vWorldPos1 = mul(matMotionBlur, vPosition);
		float3 delta_vector = (vWorldPos1 - vWorldPos).xyz;
		float maxMoveLength = length(delta_vector);
		float3 moveDirection = delta_vector / maxMoveLength; //normalize(delta_vector);
		
		if(maxMoveLength > 0.25)
		{
			maxMoveLength = 0.25;
			vWorldPos1.xyz = vWorldPos.xyz + delta_vector * maxMoveLength;
		}
		
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.12) ? 1.0 : 0.0;

		float y_factor = saturate(vPosition.y + 0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5);

		float extra_alpha = 0.1;
		float start_alpha = (1.0 + extra_alpha);
		float end_alpha = start_alpha - 1.8;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vColor.a = saturate(0.5 - vPosition.y) + alpha + 0.25;
		
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vPosition);
	}

	Out.Tex0.xy = tc;

	float3 relative_cam_pos = normalize(vCameraPos - vWorldPos).xyz;
	float2 envpos;
	float3 tempvec = relative_cam_pos - vWorldN;
	float3 vHalf = normalize(relative_cam_pos - vSunDir.xyz);
	float3 fSpecular = (spec_coef * vec4(vSunColor.rgb, 1.0) * vec4(vSpecularColor.rgb, 1.0) * pow( saturate( dot( vHalf, vWorldN) ), fMaterialPower)).xyz;
	Out.vSpecular = fSpecular;
	Out.vSpecular *= vColor.bgr;

	envpos.x = (tempvec.y);// + tempvec.x);
	envpos.y = tempvec.z;
	envpos += 1.0;
	//   envpos *= 0.5;

	Out.Tex0.zw = envpos;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);
	//shadow mapping variables
	float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	Out.SunLight.a = vColor.a;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_ENVMAP_SPECULAR vs_envmap_specular_Instanced(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor,
													   float3 vInstanceData0, float3 vInstanceData1, float3 vInstanceData2, float3 vInstanceData3)
{
	VS_OUTPUT_ENVMAP_SPECULAR Out;

	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);

	float4 vWorldPos = mul(matWorldOfInstance, vPosition);
	float3 vWorldN = normalize(mul(matWorldOfInstance, vec4(vNormal, 0.0)).xyz);	
	
	if(bUseMotionBlur)	//motion blur flag!?!
	{
		float4 vWorldPos1;
		float3 moveDirection;
		if(true)	//instanced meshes dont have valid matMotionBlur!
		{
			const float blur_len = 0.2;
			moveDirection = -normalize( float3(matWorldOfInstance[0][0],matWorldOfInstance[1][0],matWorldOfInstance[2][0]) );	//using x axis !
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		}
		else
		{
			vWorldPos1 = mul(matMotionBlur, vPosition);
			moveDirection = normalize(vWorldPos1 - vWorldPos).xyz;
		}
		
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.12) ? 1.0 : 0.0;

		float y_factor = saturate(vPosition.y + 0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5);

		float extra_alpha = 0.1;
		float start_alpha = (1.0+extra_alpha);
		float end_alpha = start_alpha - 1.8;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vColor.a = saturate(0.5 - vPosition.y) + alpha + 0.25;
	}
	
	Out.Pos = mul(matViewProj, vWorldPos);

	Out.Tex0.xy = tc;

	float3 relative_cam_pos = normalize(vCameraPos - vWorldPos).xyz;
	float2 envpos;
	float3 tempvec = relative_cam_pos - vWorldN;
	float3 vHalf = normalize(relative_cam_pos - vSunDir.xyz);
	float3 fSpecular = pow(saturate(dot(vHalf, vWorldN)), fMaterialPower) * spec_coef * vSunColor.rgb * vSpecularColor.rgb;
	Out.vSpecular = fSpecular;
	Out.vSpecular *= vColor.bgr;

	envpos.x = (tempvec.y);// + tempvec.x);
	envpos.y = tempvec.z;
	envpos += 1.0;
	//   envpos *= 0.5;

	Out.Tex0.zw = envpos;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);


	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);
	//shadow mapping variables
	float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	Out.SunLight.a = vColor.a;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matView, vWorldPos).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_BUMP_DYNAMIC vs_main_bump_interior(float4 vPosition, float3 vNormal, float2 tc,  float3 vTangent, float3 vBinormal, float4 vVertexColor)
{
	VS_OUTPUT_BUMP_DYNAMIC Out;

	float4 vWorldPos = mul(matWorld, vPosition);
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;
   
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	#ifndef USE_LIGHTING_PASS
		float3 point_to_light = vLightPosDir[iLightIndices[0]].xyz - vWorldPos.xyz;
		Out.vec_to_light_0.xyz =  mul(TBNMatrix, point_to_light);
		point_to_light = vLightPosDir[iLightIndices[1]].xyz - vWorldPos.xyz;
		Out.vec_to_light_1.xyz =  mul(TBNMatrix, point_to_light);
		point_to_light = vLightPosDir[iLightIndices[2]].xyz - vWorldPos.xyz;
		Out.vec_to_light_2.xyz =  mul(TBNMatrix, point_to_light);
	#endif
	
	Out.VertexColor = vVertexColor.bgra;

	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_BUMP_DYNAMIC_NEW vs_main_bump_interior_new(float4 vPosition, float3 vNormal, float2 tc,  float3 vTangent, float3 vBinormal, float4 vVertexColor)
{
	VS_OUTPUT_BUMP_DYNAMIC_NEW Out;

	float4 vWorldPos = mul(matWorld, vPosition);
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	#ifndef USE_LIGHTING_PASS
		float3 point_to_light = vLightPosDir[iLightIndices[0]].xyz - vWorldPos.xyz;
		Out.vec_to_light_0.xyz = mul(TBNMatrix, point_to_light);
		point_to_light = vLightPosDir[iLightIndices[1]].xyz - vWorldPos.xyz;
		Out.vec_to_light_1.xyz = mul(TBNMatrix, point_to_light);
		point_to_light = vLightPosDir[iLightIndices[2]].xyz - vWorldPos.xyz;
		Out.vec_to_light_2.xyz = mul(TBNMatrix, point_to_light);
	#endif
	
	Out.VertexColor = vVertexColor.bgra;
	
	float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.ViewDir = mul(TBNMatrix, viewdir);

	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_CHARACTER_SHADOW vs_character_shadow(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_CHARACTER_SHADOW Out;
	
	float4 vWorldPos = mul(matWorld, vPosition);

	if (PcfMode != PCF_NONE)
	{
		//shadow mapping variables
		float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);

		float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
		Out.SunLight = wNdotSun * vec4(vSunColor.rgb, 1.0);

		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT vs_main_skin(float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vBlendWeights, float4 vBlendIndices, int PcfMode)
{
	VS_OUTPUT Out;

#ifdef DISABLE_GPU_SKINNING
	float4 vObjectPos = vPosition;
	
	float3 vObjectN = vNormal;
#else
	float4 vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
	float3 vObjectN = normalize(  mul(matWorldArray[int(vBlendIndices.x)], vec4(vNormal, 0.0)).xyz * vBlendWeights.x
								+ mul(matWorldArray[int(vBlendIndices.y)], vec4(vNormal, 0.0)).xyz * vBlendWeights.y
								+ mul(matWorldArray[int(vBlendIndices.z)], vec4(vNormal, 0.0)).xyz * vBlendWeights.z
								+ mul(matWorldArray[int(vBlendIndices.w)], vec4(vNormal, 0.0)).xyz * vBlendWeights.w);
#endif

	float4 vWorldPos = mul(matWorld, vObjectPos);
	Out.Pos = mul(matWorldViewProj, vObjectPos);
	float3 vWorldN = normalize(mul(matWorld, vec4(vObjectN, 0.0)).xyz); //normal in world space

	float3 P = mul(matView, vWorldPos).xyz; //position in view space

	Out.Tex0 = tc;

	//light computation
	Out.Color = vAmbientColor;

	//directional lights, compute diffuse color
	Out.Color.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		Out.Color += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif

	//apply material color
	Out.Color *= vMaterialColor * vColor.bgra;
	Out.Color = min(vec4(1.0), Out.Color);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = wNdotSun * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_WATER vs_main_water(float4 vPosition, float3 vNormal, float4 vColor, float2 tc,  float3 vTangent, float3 vBinormal)
{
	VS_OUTPUT_WATER Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = mul(matWorld, vPosition).xyz;
	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos);

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);

	Out.Tex0 = tc + texture_offset.xy;

	Out.LightDif = vec4(0.0); //vAmbientColor;
	float totalLightPower = 0.0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir.xyz);
	Out.LightDif += vec4(vSunColor.rgb, 1.0) * vColor.bgra;
	totalLightPower += length(vSunColor.rgb);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w) / 2.0;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;
	}
	
	return Out;
}

VS_OUTPUT_SIMPLE_HAIR vs_hair(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_SIMPLE_HAIR Out;
	
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	Out.Color = vColor * diffuse_light;

	//shadow mapping variables
	float wNdotSun = (dot(vWorldN, -vSunDir.xyz));
	float sun_light_amount = saturate( max(0.2 * (wNdotSun + 0.9), wNdotSun) );
	Out.SunLight = vec4(vSunColor.rgb * sun_light_amount, 1.0) * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_HAIR vs_hair_aniso(int PcfMode, float4 vPosition, float3 vNormal, float3 vTangent, float3 vBinormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_HAIR Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	Out.VertexLighting = saturate(vColor.bgra * diffuse_light);
	
	Out.VertexColor = vColor.bgra;
	
	if(true)
	{
		float3 Pview = (vCameraPos - vWorldPos).xyz;
		Out.normal = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);
		//Out.tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz);
		Out.tangent = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz);
		Out.viewVec = normalize(Pview);
	}
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_SIMPLE_FACE vs_face(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor)
{
	VS_OUTPUT_SIMPLE_FACE Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0))).xyz; //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//point lights
	#ifndef USE_LIGHTING_PASS
		diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = vMaterialColor * vColor.bgra * diffuse_light;

	//shadow mapping variables
	float wNdotSun = dot(vWorldN, -vSunDir.xyz);
	Out.SunLight =  max(0.2 * (wNdotSun + 0.9), wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_STANDART vs_main_standart_face_mod (int PcfMode, bool use_bumpmap, float4 vPosition, float3 vNormal, float2 tc, float3 vTangent, float3 vBinormal, float4 vVertexColor, float4 vBlendWeights, float4 vBlendIndices)
{
	VS_OUTPUT_STANDART Out;
	
	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	vObjectPos = vPosition;
	
	vObjectN = vNormal;

	if(use_bumpmap)
	{
		vObjectT = vTangent;
		vObjectB = vBinormal;
	}
		
	float4 vWorldPos = mul(matWorld, vObjectPos);
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;
	
	float3 vWorldN = normalize(mul(matWorld, vec4(vObjectN, 0.0)).xyz);
	
	float3x3 TBNMatrix;
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul(matWorld, vec4(vObjectB, 0.0)).xyz);
		float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vObjectT, 0.0)).xyz);
		TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN); 
	}
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
	}

	if(use_bumpmap)
	{
		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
		Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	}
	else
	{
		Out.SunLightDir = vWorldN;
	}

	Out.VertexColor = vVertexColor.bgra;	
	
	//point lights
	#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, true, true).xyz;
	#endif
	
	#ifndef USE_LIGHTING_PASS 
		int effective_light_index = iLightIndices[0];
		float3 point_to_light = vLightPosDir[effective_light_index].xyz - vWorldPos.xyz;
		float LD = dot(point_to_light, point_to_light);
		Out.PointLightDir.a = saturate(1.0 / LD);	//prevent bloom for 1 meters
		
		if(use_bumpmap)
		{
			Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
		}
		else
		{
			Out.PointLightDir.xyz = normalize(point_to_light);
		}
	#endif
	
	
	if(use_bumpmap)
	{
		Out.ViewDir =  mul(TBNMatrix, normalize(vCameraPos.xyz - vWorldPos.xyz));
	}
	else {
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
	}
	
	float3 P = mul(matWorldView, vObjectPos).xyz; //position in view space
	
	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_DEPTHED_FLARE vs_main_depthed_flare(float4 vPosition, float4 vColor, float2 tc)
{
	VS_DEPTHED_FLARE Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;
	
	if(use_depth_effects)
	{
		Out.projCoord.xy = (float2(Out.Pos.x, Out.Pos.y) + Out.Pos.w) / 2.0;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;
	}

	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float4 vWorldPos = mul(matWorld, vPosition);
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_MAP vs_main_map(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor.bgra;
	}

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;
	
	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0) * vMaterialColor * vColor.bgra;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos - vWorldPos).xyz;
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_MAP_BUMP vs_main_map_bump(int PcfMode, float4 vPosition, float3 vNormal, float3 vTangent, float3 vBinormal, float2 tc, float4 vColor,float4 vLightColor)
{
	VS_OUTPUT_MAP_BUMP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
	float3x3 TBNMatrix = float3x3_transpose(vWorld_tangent, vWorld_binormal, vWorldN);  
	
	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	diffuse_light += vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;
	
	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);
	Out.Color.a = vMaterialColor.a * vColor.a;

	//shadow mapping variables

	//move sun light to pixel shader
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor.rgb * vMaterialColor * vColor;
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos - vWorldPos).xyz;
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_MAP_MOUNTAIN vs_map_mountain(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_MOUNTAIN Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0.xy = tc;
	Out.Tex0.z = /*saturate*/(0.7 * (vWorldPos.z - 1.5));

	float4 diffuse_light = vAmbientColor;
	diffuse_light += vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vec4(vSunColor.rgb, 1.0);
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos - vWorldPos).xyz;
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_MAP_MOUNTAIN_BUMP vs_map_mountain_bump(int PcfMode, float4 vPosition, float3 vNormal,  float3 vTangent, float3 vBinormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_MOUNTAIN_BUMP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0.xy = tc;
	Out.Tex0.z = (0.7 * (vWorldPos.z - 1.5));

	float4 diffuse_light = vAmbientColor;
	diffuse_light += vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);
	Out.Color.a = vMaterialColor.a * vColor.a;

	//shadow mapping variables
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
			
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos - vWorldPos).xyz;
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_MAP_WATER vs_map_water(bool reflections, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_WATER Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc + texture_offset.xy;

	float4 diffuse_light = vAmbientColor + vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	float wNdotSun = max(0.0001, dot(vWorldN, -vSunDir.xyz));
	diffuse_light.rgb += (wNdotSun) * vSunColor.rgb;
	diffuse_light.a = 1.0;

	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra) * diffuse_light;
	
	if(reflections)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y) + water_pos.w) / 2.0;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}
	
	vWorldN = float3(0.0, 0.0, 1.0); //vNormal; //normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_tangent = float3(1.0, 0.0, 0.0); //normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3 vWorld_binormal = float3(0.0, 1.0, 0.0); //normalize(cross(vWorld_tangent, vNormal)); //normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
	Out.LightDir = mul(TBNMatrix, -vSunDir.xyz);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}

VS_OUTPUT_MAP_FONT vs_map_font(float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_FONT Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor + vLightColor.bgra;
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;
	diffuse_light.rgb += saturate(dot(vWorldN, -vSunDir.xyz)) * vSunColor.rgb;
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	//extra for fading out txt on world map
	float3 view_vec2 = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Map = length(view_vec2);

	return Out;
}

VS_OUTPUT_PARALLAX_WATER vs_parallax_water(float4 vPosition, float3 vNormal, float4 vColor, float2 tc, float3 vTangent, float3 vBinormal)
{
	VS_OUTPUT_PARALLAX_WATER Out;

	//CUSTOM TIME VARIABLE - SET BY PHAIK
	float Timer = GetTimer(1.0);
	
	//WAVE INFORMATION - SET BY PHAIK
	float4 WaveInfo = GetWaveInfo();
	float2 Amplitude = WaveInfo.xy;
	float2 Period = WaveInfo.zw;
	
	//INITIAL WAVE ORIGIN - SET BY PHAIK	
	float4 Origin = GetWaveOrigin();

	// Waves on y axis
	vPosition.z = (vPosition.z + Amplitude.y * sin((Period.y *  vPosition.y) + Timer) + Origin.y); //
	// Waves on x axis
	vPosition.z = (vPosition.z + Amplitude.x * sin((Period.x *  vPosition.x) + Timer) + Origin.x); //
	//OVERALL SEA LEVEL
	vPosition.z = vPosition.z + Origin.z;
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = mul(matWorld, vPosition).xyz;
	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos);

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);
	
	//insert from parallax shader
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz);
	
    float fresnel = 1.0 - (saturate(dot(vViewDir, vWorldN)));
    fresnel*=fresnel + 0.1;
  
    // yay for TBN space
    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir.xy = vViewDir.xy;
	 
	Out.Tex0 = tc * 1.75;

	Out.LightDif = float4(0.0); //vAmbientColor;
	float totalLightPower = 0.0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir.xyz);
	Out.LightDif += vSunColor * vColor.bgra;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w) / 2.0;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;
	}
	
	float3 view_vector = (vCameraPos.xyz - vWorldPos.xyz);
	//Out.Depth.y = length(view_vector);
	
	return Out;
}

VS_OUTPUT_PARALLAX_WATER vs_outer_terrain_water(float4 vPosition, float3 vNormal, float4 vColor, float2 tc,  float3 vTangent, float3 vBinormal)
{
	VS_OUTPUT_PARALLAX_WATER Out;
	
	vPosition.z = vPosition.z + 2.7;
		
	Out.Pos = mul(matWorldViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = mul(matWorld, vPosition).xyz;
	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos);

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);
	
	//insert from parallax shader
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	
    float fresnel = 1.0 - (saturate(dot(vViewDir, vWorldN)));
    fresnel*=fresnel + 0.1;
  
    // yay for TBN space
    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir.xy = vViewDir.xy;
	 
	Out.Tex0 = tc;

	Out.LightDif = float4(0.0); //vAmbientColor;
	float totalLightPower = 0.0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir.xyz);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w) / 2.0;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;
	}
	
	float3 view_vector = (vCameraPos.xyz - vWorldPos.xyz);
	
	return Out;
}

VS_OUTPUT_SEA_FOAM vs_main_sea_foam(int PcfMode, bool UseSecondLight, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_SEA_FOAM Out;
	
	//CUSTOM TIME VARIABLE - SET BY PHAIK
	float Timer = GetTimer(1.0);
	
	//WAVE INFORMATION - SET BY PHAIK
	float4 WaveInfo = GetWaveInfo();
	float2 Amplitude = WaveInfo.xy;
	float2 Period = WaveInfo.zw;
	
	//INITIAL WAVE ORIGIN - SET BY PHAIK	
	float4 Origin = GetWaveOrigin();

	vPosition.z = (vPosition.z + Amplitude.y * sin((Period.y *  vPosition.y) + Timer) + Origin.y); //
	// Waves on x axis
	vPosition.z = (vPosition.z + Amplitude.x * sin((Period.x *  vPosition.x) + Timer) + Origin.x); //
	//OVERALL SEA LEVEL
	vPosition.z = vPosition.z + Origin.z;
	
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	Out.Tex0.xy = tc;
	
	Out.Tex0.z = (0.7 * (vWorldPos.z - 1.5));
	Out.Tex0.w = vWorldPos.x;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_BUMP vs_main_bump_bark (int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float3 vTangent, float3 vBinormal, float4 vVertexColor, float4 vPointLightDir)
{
	VS_OUTPUT_BUMP Out;

	float4 WorldPosit = mul(matWorld, vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0, vPosition.z);; //range of 0 to 3

	float dx_tc_y = 1.0 - tc.y;
	
	if(dx_tc_y < 0.90)
	{
		float timer_variable = tree_rate * time_var;
		float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
		float2 OriginalPosition = float2(vPosition.x,vPosition.y);

		float treeamp = (saturate(pow((1.0 - dx_tc_y) + 0.2, 2.0))) * TreeAmplitude.x;
		treeamp *= WindFactor;
		vPosition.x = vPosition.x + treeamp * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
		
		vPosition.x = vPosition.x + treeamp * sin((TreePeriod.x * 0.5)  * WorldPosition.x + (0.2 * timer_variable)); //
		vPosition.y = vPosition.y + treeamp * sin((TreePeriod.x * 0.76)  * WorldPosition.x + (1.1 * timer_variable)); //
		
		vPosition.z -= 0.3 * (OriginalPosition.x - vPosition.x);
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir.xyz);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0 * vPointLightDir.rgb - 1.0;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor.bgra;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	//Out.ViewDir = mul(TBNMatrix, Out.ViewDir);

	Out.WorldNormal = vWorldN;
	//Out.WorldNormal = mul(TBNMatrix, Out.WorldNormal);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_PARALLAX vs_main_parallax(int PcfMode, float4 vPosition, float3 vNormal, float2 tc, float3 vTangent, float3 vBinormal, float4 vVertexColor, float4 vPointLightDir)
{
	VS_OUTPUT_PARALLAX Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float4 vWorldPos = mul(matWorld, vPosition);
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir.xyz);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0 * vPointLightDir.rgb - 1.0;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor.bgra;
		
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 

    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir = vViewDir;

	Out.WorldNormal.xyz = vWorldN;
	Out.WorldNormal.w = 1.0 - (saturate(dot(vViewDir, vWorldN))); //.z is fresnel

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_STANDART vs_main_standart_sails (int PcfMode, bool use_bumpmap, bool use_skinning, float4 vPosition,
											float3 vNormal, float2 tc,  float3 vTangent, float3 vBinormal,
											float4 vVertexColor, float4 vBlendWeights, float4 vBlendIndices)
{
	VS_OUTPUT_STANDART Out;
	
	float4 vPos_without_movement = vPosition;
	float WindFactor = GetWindAmount(1.0);
	float WindRotation = GetWindDirection(1.0);
	float2 UV;
	UV.x = tc.x;
	UV.y = 1.0 - tc.y;
	
    // below line defines 9 sections/ points where the vertices should not move
	// left bottom (actually top) 		|| left middle 										|| left top 							|| middle bottom  									|| middle middle 													|| middle top 											|| and so on
	if(((UV.y < 0.05) && (UV.x < 0.05)) || ((UV.x > 0.95) && (UV.y < 0.05)) || (UV.y > 0.95))
	{
		vPosition.x = 	vPosition.x;
	}
	else //if not in the fixed sections of uv map then we can wave
	{
		float3 vecObjectPos = vNormal;
		float4 vecWorldPositiom = mul(matWorld, vPosition);
		float4 vecObjPositiom = mul(matWorld, vPosition);
		float3 vecWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
		float3 vecWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //normal in world space
		float3 vecWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //normal in world space
		float3x3 TBNMatrix = float3x3(vecWorld_tangent, vecWorld_binormal, vecWorldN); 
		
		//define north
		float3 NorthDir;
		NorthDir.x = 0.001;
		NorthDir.y = 0.99;
		NorthDir.z = 0.001;
		
		//initially set wind direction to north
		float4 WindDir = float4(1.0);
		WindDir.xyz = NorthDir;
		
		//get degrees to rotate wind direction
		float radians = WindRotation * 0.0174532925; //convert degrees to radians
		
		//ROTATE Wind direction from north to actual direction of wind // ROTATE VECTOR ON Z AXIS EQUATION
		WindDir.x = (cos(radians)*NorthDir.x) - (sin(radians)*NorthDir.y);
		WindDir.y = (sin(radians)*NorthDir.x) + (cos(radians)*NorthDir.y);
		
		float4 WindDirection = float4(1.0);
		WindDirection.xyz = mul(TBNMatrix, WindDir.xyz);

		float ObjdotWind = (dot(vecObjectPos.xy, WindDirection.xy)); // gets angle between object and wind direction
		//  1 and minus 1 - face normal is perpendicular to wind dir, 0 - face normal is parallel to wind dir
		
		float inflate = ObjdotWind;
		if (inflate < 0.0) //takes negatives and makes them positive so scale is from 0 (normal is parallel to wind dir) to 1 (normal is perpendicular to wind dir)
		{
			inflate = 0.0 - inflate;
		}

		inflate *= WindFactor;
		 
		vPosition.x += ((inflate / 6.0)) * sin(1.5* vPosition.y + (1.6 * WindFactor) * time_var);//inflate is 0 (normal is parallel to wind dir) to 1 (normal is perpendicular to wind dir)
	    vPosition.x += ((inflate / 4.0)) * sin(0.6* vPosition.y +  WindFactor * time_var); //creates wave moving along sails on y axis (side to side)
		
		inflate = 1.0 - inflate; //inverse so that inflate is 0 (normal is perpendicular to wind dir) to 1 (normal is parallel to wind dir)
		vPosition.x += ((inflate / 4.0)) * sin(0.6* vPosition.z + WindFactor * time_var); //creates wave moving down sails on z axis
	}

	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	if(use_skinning)
	{
		vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
		
		vObjectN = normalize(  mul(matWorldArray[int(vBlendIndices.x)], vec4(vNormal, 0.0)).xyz * vBlendWeights.x
								+ mul(matWorldArray[int(vBlendIndices.y)], vec4(vNormal, 0.0)).xyz * vBlendWeights.y
								+ mul(matWorldArray[int(vBlendIndices.z)], vec4(vNormal, 0.0)).xyz * vBlendWeights.z
								+ mul(matWorldArray[int(vBlendIndices.w)], vec4(vNormal, 0.0)).xyz * vBlendWeights.w);
									
		if(use_bumpmap)
		{
			vObjectT = normalize(  mul(matWorldArray[int(vBlendIndices.x)], vec4(vTangent, 0.0)).xyz * vBlendWeights.x
									+ mul(matWorldArray[int(vBlendIndices.y)], vec4(vTangent, 0.0)).xyz * vBlendWeights.y
									+ mul(matWorldArray[int(vBlendIndices.z)], vec4(vTangent, 0.0)).xyz * vBlendWeights.z
									+ mul(matWorldArray[int(vBlendIndices.w)], vec4(vTangent, 0.0)).xyz * vBlendWeights.w);
			
			vObjectB = cross(vObjectN, vObjectT);	
			bool left_handed = (dot(cross(vNormal,vTangent),vBinormal) < 0.0);
			if(left_handed)
			{
				vObjectB = -vObjectB;
			}
		}
	}
	else
	{
		vObjectPos = vPosition;
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = vTangent;
			vObjectB = vBinormal;
		}
	}
	
	float4 vWorldPos = mul(matWorld, vObjectPos);
	float3 vWorldN = normalize(mul(matWorld, vec4(vObjectN, 0.0)).xyz);
	
	bool use_motion_blur = bUseMotionBlur && (!use_skinning);
	
	if(use_motion_blur)	//motion blur flag!?!
	{
		#ifdef STATIC_MOVEDIR //(used in instanced rendering )
			const float blur_len = 0.25;
			float3 moveDirection = -normalize( float3(matWorld[0][0], matWorld[1][0], matWorld[2][0]) );
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			float4 vWorldPos1 = vWorldPos + float4(moveDirection, 0.0) * blur_len;
		#else 
			float4 vWorldPos1 = mul(matMotionBlur, vObjectPos);
			float3 moveDirection = normalize(vWorldPos1.xyz - vWorldPos.xyz);
		#endif
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.1) ? 1.0 : 0.0;

		float y_factor = saturate(vObjectPos.y + 0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5);

		float extra_alpha = 0.1;
		float start_alpha = (1.0 + extra_alpha);
		float end_alpha = start_alpha - 1.8;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vVertexColor.a = saturate(0.5 - vObjectPos.y) + alpha + 0.25;
	}

	if(use_motion_blur)
	{
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vObjectPos);
	}

	Out.Tex0 = tc;
	
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul(matWorld, vec4(vObjectB, 0.0)).xyz);
		float3 vWorld_tangent = normalize(mul(matWorld, vec4(vObjectT, 0.0)).xyz);
		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
		Out.SkyLightDir = mul(TBNMatrix, float3(0.0, 0.0, 1.0)); //STR_TEMP!?
		Out.VertexColor = vVertexColor.bgra;
		
		//point lights
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, true).xyz;
		#endif
		
		#ifndef USE_LIGHTING_PASS 
		float3 point_to_light = vLightPosDir[iLightIndices[0]].xyz - vWorldPos.xyz;
		Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
		
		float LD = dot(point_to_light, point_to_light);
		Out.PointLightDir.a = saturate(1.0 / LD);	//prevent bloom for 1 meters
		#endif
		
		float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.ViewDir =  mul(TBNMatrix, viewdir);
		
		#ifndef USE_LIGHTING_PASS
		if (PcfMode == PCF_NONE)
		{
			Out.ShadowTexCoord = calculate_point_lights_specular(vWorldPos.xyz, vWorldN, viewdir, true);
		}
		#endif
	}
	else
	{
		Out.VertexColor = vVertexColor.bgra;
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false).xyz;
		#endif
		
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
		
		Out.SunLightDir = vWorldN;
		#ifndef USE_LIGHTING_PASS
		Out.SkyLightDir = calculate_point_lights_specular(vWorldPos.xyz, vWorldN, Out.ViewDir, false).xyz;
		#endif
	}
	
	Out.VertexColor.a *= vMaterialColor.a;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vObjectPos).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
		
	return Out;
}

VS_OUTPUT_HAIR vs_hair_aniso_static(int PcfMode, float4 vPosition, float3 vNormal, float3 vTangent, float2 tc, float4 vColor)
{
	VS_OUTPUT_HAIR Out;

	float2 Period = float2(25.0, 20.0);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	float2 sintc = tc + 0.01 * float2(sin(Period.x *  tc.y + 1.5 * time_var), 0.0);
	Out.Tex0 = sintc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	Out.VertexLighting = saturate(vColor * diffuse_light);
	
	Out.VertexColor = vColor;
	
	if(true)
	{
		float3 Pview = (vCameraPos - vWorldPos).xyz;
		Out.normal = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz).xyz; //normal in world space
		Out.tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz).xyz; //normal in world space
		Out.viewVec = normalize(Pview);
	}
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_FLORA_SEASON vs_flora_season(int PcfMode, float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_SEASON Out;
	
	float4 WorldPosit = mul(matWorld, vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0, vPosition.z); //range of 0 to 3
		
	float2 WorldPosition = float2(WorldPosit.z, WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float timer_variable = tree_rate * time_var;
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.76) * WorldPosition.x + ((1.1*timer_variable))); //
	
	float delta_pos = OriginalPosition.x-vPosition.x;
	vPosition.z -= 0.3 * delta_pos;
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float dx_tc_y = 1.0 - tc.y;
	coords.x = tc.x + ((WindFactor*1.5*(0.033* (1.0-dx_tc_y))) * sin(5.0 * (1.0-dx_tc_y) + 1.75*timer_variable)); //
	coords.x = coords.x + ((WindFactor*1.5*(0.10* (1.0-dx_tc_y))) * sin(5.0 * (1.0-dx_tc_y) + 0.25*timer_variable)); //
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();
    coords.x +=  0.015 * moveamount;
    coords.x = lerp(coords.x, tc.x, saturate(dx_tc_y * dx_tc_y + 0.1));
	
	Out.Tex0 = coords;
	Out.Color = vColor.bgra * (vAmbientColor + vec4(vSunColor.rgb, 1.0) * 0.06); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34) * vMaterialColor * vColor.bgra;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA_SEASON_NO_SHADOW vs_flora_season_no_shadow(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_SEASON_NO_SHADOW Out;
	
	float4 WorldPosit = mul(matWorld, vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0, vPosition.z); //range of 0 to 3
	
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float timer_variable = tree_rate * time_var;
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.76) * WorldPosition.x + ((1.1*timer_variable))); //
	
	vPosition.z -= 0.3 * (OriginalPosition.x-vPosition.x);

	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld,vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float dx_tc_y = 1.0 - tc.y;
	coords.x = tc.x + ((0.033* (1.0-dx_tc_y)) * sin(5.0 * (1.0-dx_tc_y) + 1.75*timer_variable)); //
	coords.x = coords.x + ((0.10* (1.0-dx_tc_y)) * sin(5.0 * (1.0-dx_tc_y) + 0.25*timer_variable)); //
	
	Out.Tex0 = coords;
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA_SEASON vs_flora_season_grass(int PcfMode, float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_SEASON Out;

	float4 WorldPosit = mul(matWorld, vPosition);
	float timer_variable = tree_rate * time_var;
	float WindFactor = 0.333 * GetWindAmountNew(1.0, vPosition.z); //range of 0 to 3
	
	float texcordY = 1.0 - tc.y;
	if ((tc.y < 0.15)||((tc.y > 0.165) && (tc.y < 0.320))||((tc.x > 0.500) && (tc.y > 0.330) && (tc.y < 0.640)))
	{
		float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
		float2 OriginalPosition = float2(vPosition.x,vPosition.y);
		vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
		vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.5) * WorldPosition.x + ((0.2*timer_variable))); //
		vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.76) * WorldPosition.x + ((1.1*timer_variable))); //
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x, tc.y);
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();
    coords.x +=  0.015 * moveamount;

	float dx_tc_y = 1.0 - tc.y;
    coords.x = lerp(coords.x, tc.x, saturate(dx_tc_y * dx_tc_y + 0.1));
	
	Out.Tex0 = coords;

	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	Out.Color.a = Out.Color.a * min(1.0,(1.0 - (d / 50.0)) * 2.0);

	return Out;
}

VS_OUTPUT_FLORA_SEASON_NO_SHADOW vs_flora_season_grass_no_shadow(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_SEASON_NO_SHADOW Out;
	
	float4 WorldPosit = mul(matWorld, vPosition);
	float timer_variable = tree_rate * time_var;
	float WindFactor = 0.333 * GetWindAmountNew(1.0, vPosition.z); //range of 0 to 3
	
	float texcordY = 1.0 - tc.y;
	if ((tc.y < 0.15)||((tc.y > 0.165) && (tc.y < 0.320))||((tc.x > 0.500) && (tc.y > 0.330) && (tc.y < 0.640)))
	{
		float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
		float2 OriginalPosition = float2(vPosition.x,vPosition.y);
		vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
		vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.5) * WorldPosition.x + ((0.2*timer_variable))); //
		vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.76) * WorldPosition.x + ((1.1*timer_variable))); //
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();
    coords.x +=  0.015 * moveamount;

	float dx_tc_y = 1.0 - tc.y;
    coords.x = lerp(coords.x, tc.x, saturate(dx_tc_y * dx_tc_y + 0.1));

	Out.Tex0 = coords;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	Out.Color.a = min(1.0,(1.0 - (d / 50.0)) * 2.0);

	return Out;
}

VS_OUTPUT_FLORA_MAP vs_flora_map(int PcfMode, float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_MAP Out;

	float3 vecObjectPos = vPosition.xyz;
	float4 vecWorldPositiom = mul(matWorld, vPosition);
	//change to objspacce / vpos is in worldspace

	vPosition.z += 0.01 * sin(0.7 * vPosition.y + 0.5 * time_var);
	vPosition.x += 0.015 * sin(0.9 * vPosition.y + 0.4 * time_var);
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);
	Out.WorldPos = vWorldPos.xy;

	Out.Tex0.xy = tc;
	
	Out.Tex0.xy = tc;
	Out.Tex0.z = (0.7 * (vWorldPos.z - 1.5));
	Out.Tex0.w = vWorldPos.x;
	
	Out.Color = vColor.bgra * (vAmbientColor + vec4(vSunColor.rgb, 1.0) * 0.06); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34) * vMaterialColor * vColor.bgra;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_FLORA_NO_SHADOW vs_flora_map_no_shadow(float4 vPosition, float4 vColor, float2 tc)
{
	VS_OUTPUT_FLORA_NO_SHADOW Out;
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = mul(matWorld, vPosition);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor.bgra * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

VS_OUTPUT_NEW_MAP vs_new_map(int PcfMode, float4 vPosition, float3 vNormal, float3 vTangent, float3 vBinormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_NEW_MAP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz);
	float3 vWorld_tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz);
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	Out.Tex0.xy = tc;
	Out.Tex0.z = (0.7 * (vWorldPos.z - 1.5));
	Out.Tex0.w = vWorldPos.x;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor.bgra;
	}

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;
	
	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra * diffuse_light);

	//shadow mapping variables

	//move sun light to pixel shader
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir.xyz));
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos - vWorldPos).xyz;
	Out.CameraDir = mul(TBNMatrix, -Out.ViewDir.xyz);
	
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_MAP_WATER vs_map_foam (bool reflections, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_WATER Out;

	float2 Amplitude = float2(0.2, 1.0);
	float2 Period = float2(20.0, 10.0);
	
	float2 WorldPosition = float2(tc.x, tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	if (vPosition.z < 0.7)
	{
		vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
		vPosition.z = vPosition.z + Amplitude.y * sin(Period.y *  WorldPosition.y + time_var); //
	}
		
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor + vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
	diffuse_light.rgb += (wNdotSun) * vSunColor.rgb;

	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra) * diffuse_light;
	
	Out.PosWater = vWorldPos;
	
	vWorldN = float3(0.0, 0.0, 1.0);
	float3 vWorld_tangent  = float3(1.0, 0.0, 0.0);
	float3 vWorld_binormal = float3(0.0, 1.0, 0.0);

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
	Out.LightDir = mul(TBNMatrix, -vSunDir.xyz);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}

VS_OUTPUT_MAP_WATER_NEW vs_map_water_new (bool reflections, float4 vPosition, float3 vNormal, float3 vTangent, float3 vBinormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_WATER_NEW Out;

	float4 vWorldPosNoMove = mul(matWorld, vPosition);
	
	float2 Amplitude = float2(0.07,0.08);
	float2 Period = float2(20.0, 13.0);
	float2 WorldPosition = float2(tc.x,tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	if (vPosition.z < 0.7)
	{
		vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
		vPosition.z = vPosition.z + Amplitude.y * sin(Period.y *  WorldPosition.y + time_var); //
	}

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	
	//parallax
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz);
	float3 vWorld_tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz);
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = 0.065 * float2(vWorldPos.x,vWorldPos.y);
    Out.Tex0.y *= 0.75;

	float4 diffuse_light = vAmbientColor + vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light.rgb += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor.rgb;

	float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
	diffuse_light.rgb += (wNdotSun) * vSunColor.rgb;

	Out.Color = (vMaterialColor * vColor.bgra) * diffuse_light;
	Out.Color.w = vWorldPosNoMove.z;
	
	if(false/*reflections*/)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y) + float2(water_pos.w)) / 2.0;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}

	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);

    Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y) + float2(Out.Pos.w)) / 2.0;
	Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
	Out.projCoord.zw = Out.Pos.zw;
	Out.Depth.x = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;

	Out.LightDif = float4(0.0); //vAmbientColor;
	float totalLightPower = 0.0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir.xyz);
	Out.LightDif.rgb += vSunColor.rgb * vColor.bgr;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;
		
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Depth.y = length(view_vec);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}

VS_OUTPUT_MAP_WATER_NEW vs_map_water_river_new(bool reflections, float4 vPosition, float3 vNormal, float3 vTangent, float3 vBinormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_MAP_WATER_NEW Out;
	
	float2 Amplitude = float2(0.2, 1.0);
	float2 Period = float2(20.0, 10.0);
	float2 WorldPosition = float2(tc.x, tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	if (vPosition.z < 0.95)
	{
		vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
	}

	vPosition.z = vPosition.z - 5.5;
	 
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	
	//parallax
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz);
	float3 vWorld_tangent = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz);
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = 0.065 * float2(vWorldPos.x, vWorldPos.y);
    Out.Tex0.y *= 0.75;

	float4 diffuse_light = vAmbientColor + vLightColor.bgra;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor;

	float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir.xyz));
	diffuse_light += wNdotSun * vSunColor;

	//apply material color
	Out.Color = (vMaterialColor * vColor.bgra) * diffuse_light;
	
	//if(reflections)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y) + water_pos.w) / 2.0;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}

	Out.PosWater = mul(matWaterWorldViewProj, vPosition);
	{
		float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
	}

    Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w) / 2.0;
	Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
	Out.projCoord.zw = Out.Pos.zw;
	Out.Depth.x = ((0.5 * Out.Pos.z) + 0.5) * far_clip_Inv;
		
	Out.LightDif = float4(0.0);

	float totalLightPower = 0.0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir.xyz);
	Out.LightDif += vec4(vSunColor.rgb, 1.0) * vColor.bgra;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;
		
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Depth.y = length(view_vec);
		
	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}

VS_OUTPUT_ICON_SEASONAL vs_main_icon_seasonal(int PcfMode, bool UseSecondLight, float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float4 vLightColor)
{
	VS_OUTPUT_ICON_SEASONAL Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz);

	Out.Tex0.xy = tc;
	
	Out.Tex0.z = (0.7 * (vWorldPos.z - 1.5));
	Out.Tex0.w = vWorldPos.x;

	float4 diffuse_light = vAmbientColor;

	if (UseSecondLight)
	{
		diffuse_light += vLightColor.bgra;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir.xyz)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir.xyz));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		#ifdef SET_SHADOWCOORD_W_TO_1
			Out.ShadowTexCoord.z /= ShadowPos.w;
			Out.ShadowTexCoord.w = 1.0;
		#endif
		
		#ifdef USE_ShadowTexelPos_INTERPOLATOR
			Out.ShadowTexelPos = Out.ShadowTexCoord.xy * fShadowMapSize;
		#endif
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT_FONT_X_BUMP vs_main_no_shadow_bump(float4 vPosition, float3 vNormal, float2 tc, float4 vColor, float3 vTangent, float3 vBinormal)
{
	VS_OUTPUT_FONT_X_BUMP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = mul(matWorld, vPosition);
	float3 vWorldN = normalize(mul(matWorld, vec4(vNormal, 0.0)).xyz); //normal in world space
	float3 vWorld_binormal = normalize(mul(matWorld, vec4(vBinormal, 0.0)).xyz); //binormal in world space
	float3 vWorld_tangent  = normalize(mul(matWorld, vec4(vTangent, 0.0)).xyz); //tangent in world space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.Tex0 = tc;
	
	Out.SkyDir = mul(TBNMatrix, -vSkyLightDir.xyz);
	Out.SunDir = mul(TBNMatrix, -vSunDir.xyz);
	Out.vColor = vColor;

	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}
