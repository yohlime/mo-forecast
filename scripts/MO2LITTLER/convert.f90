!**************************************************************************!
!This program converts observation data to Little_R format readable by WRF*!
!Revsion:May 09,2014							   !
!Lyndon Mark P. Olaguera	                                           !
!Files needed: 								   !
!coordinates.csv--a file containing the coordinates of the station         !
!including terrain elevation					           !	
!txt file containing observation data		   !
!**************************************************************************!

program convertR
  implicit none

  character(*),parameter	:: coords_file_name ="coordinates_data.csv"
  character(26)			:: out_file_name
				
  integer,parameter		:: coords_file_unit = 20, &
  				csv_file_unit = 10, &
				out_file_unit = 30
  character(40),parameter	:: stninfo="SURFACE DATA FROM MO", &
				platform = "FM-12 SYNOP", &
				source = "SURFOB"
  integer,parameter		:: num_vld_fld = 8, &
				num_error = 0, &
				num_warning = 0, &
				seq_num = 0, &
				num_dups = 0, &
				sut = 0, &
				julian = 0
  logical,parameter		:: is_sound = .false., &
				bogus = .false., &
				discard = .false.
  integer		:: coords_file_status, coords_record_status
  character(40)		:: stnname
  real   		:: xlat, xlon
  real			:: stnelev
  
!  character(len=20)	:: csv_file_name 
  integer,parameter	:: datacnt = 300, &
			varcnt = 8
  character(*),parameter	:: hdr_fmt =  ' ( 2f20.5, 4a40 , f20.5 , 5i10 , 3L10 , 2i10 , a20 ,  13( f13.5 , i7 ) ) ', &
	rcd_fmt =  ' ( 10( f13.5 , i7 )) ', &
	end_fmt =  ' ( 3i7 ) '
  
  integer			:: csv_file_status, csv_record_status

  integer	:: stn , yy, mm, dd, hh
  real		:: W,WD,T,u,v,p,R,RH

  character(14) date_char
  integer	:: i
  integer	:: out_file_status, out_record_status

  open (coords_file_unit, file=coords_file_name, status='old', iostat=coords_file_status)
  if (coords_file_status /= 0) stop
  read (coords_file_unit, *)
  do
    read(coords_file_unit,*,iostat=coords_file_status) stnname, xlat, xlon, stnelev
    if (coords_file_status /= 0) exit
    
    open (csv_file_unit, file=trim(stnname)//".csv", status='old', iostat=csv_file_status)
    read (csv_file_unit, *)
    i = 1
    do
      read(csv_file_unit,*,iostat=csv_file_status)stn,yy,mm,dd,hh,T,W,WD,u,v,p,R,RH

      if (csv_file_status/= 0) exit
    out_file_name = setfilename(yy,mm,dd,hh)	
    open (out_file_unit, file=out_file_name, access='append', iostat=out_file_status)
 
    write(date_char(1:4),fmt='(i4)') yy

    if (mm < 10) then
      write(date_char(5:6),fmt='("0",i1)') mm
    else
      write(date_char(5:6),fmt='(i2)') mm
    end if

    if (dd < 10) then
      write(date_char(7:8),fmt='("0",i1)') dd
    else
      write(date_char(7:8),fmt='(i2)') dd
    end if

    if (hh < 10) then
      write(date_char(9:10),fmt='("0",i1)') hh
    else
      write(date_char(9:10),fmt='(i2)') hh
    end if

    write(date_char(11:14),fmt='("0000")')

      p = p*100.
      T =T + 273.15
      write (out_file_unit, fmt = hdr_fmt ) &
	xlat, xlon, &
	stninfo, stnname, platform, source, &
	stnelev, &
	num_vld_fld, num_error, num_warning, &
	seq_num, num_dups, &
	is_sound, bogus, discard, &
	sut, julian, date_char , &
	p,0, &
	-888888.,0, -888888.,0, -888888.,0, -888888.,0, &
	-888888.,0, -888888.,0, -888888.,0, -888888.,0, &
	-888888.,0, -888888.,0, -888888.,0, -888888.,0

    write (out_file_unit, fmt = rcd_fmt) &
	p, 10, stnelev, 10, T, 10, -888888., 0, W, 10, WD, 10, &
	u, 10, v, 10, RH, 10, -888888., 0
    write (out_file_unit, fmt = rcd_fmt) &
	-777777., 0, -777777., 0, &  
	-888888., 0,-888888., 0,-888888., 0,-888888., 0, &
	-888888., 0, -888888., 0, -888888., 0, -888888., 0
    write (out_file_unit, fmt = end_fmt) num_vld_fld, 0, 0
    close(out_file_unit)
    i = i + 1
    end do
  end do

contains 

function setfilename(yr,mo,da,hr) result(filename)
integer :: yr,mo,da,hr

character(len=26) :: filename


write(filename(1:13),fmt='(A13)')'obs_MOstns_r_'
write(filename(14:17),fmt='(i4)')yr
write(filename(18:18),fmt='(A1)')'-'
write(filename(21:21),fmt='(A1)')'-'
write(filename(24:24),fmt='(A1)')'_'
if (mo < 10) then
        write(filename(19:20),fmt='("0",i1)') mo
      else
        write(filename(19:20),fmt='(i2)') mo
      end if
      if (da < 10) then
        write(filename(22:23),fmt='("0",i1)') da
      else
        write(filename(22:23),fmt='(i2)') da
      end if
      if (hr < 10) then
        write(filename(25:26),fmt='("0",i1)') hr
      else
        write(filename(25:26),fmt='(i2)') hr
      end if
end function setfilename


end program convertR

