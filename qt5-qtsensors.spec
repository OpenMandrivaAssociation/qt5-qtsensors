%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta rc

%define qtsensors %mklibname qt%{api}sensors %{major}
%define qtsensorsd %mklibname qt%{api}sensors -d

%define qttarballdir qtsensors-opensource-src-%{version}%{?beta:-%{beta}}
%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtsensors
Summary:	Qt5 - Sensors component
Version:	5.5.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
License:	LGPLv2 with exceptions or GPLv3 with exceptions
Url:		http://qt-project.org/
BuildRequires:	qt5-qtbase-devel >= %{version}
BuildRequires:	pkgconfig(Qt5Qml)
BuildRequires:	pkgconfig(Qt5Quick)

%description
The Qt Sensors API provides access to sensor hardware via QML and C++
interfaces.  The Qt Sensors API also provides a motion gesture recognition
API for devices.

#----------------------------------------------------------------------------

%package -n	%{qtsensors}
Summary:	Qt Sensors library
Group:		System/Libraries

%description -n %{qtsensors}
Qt Sensors library.

%files -n %{qtsensors}
%{_qt5_libdir}/libQt%{api}Sensors.so.%{major}*
%{_qt5_prefix}/qml/QtSensors
%{_qt5_plugindir}/sensorgestures
%{_qt5_plugindir}/sensors

#----------------------------------------------------------------------------

%package -n %{qtsensorsd}
Summary:	Development files for the QtSensors library
Group:		Development/KDE and Qt
Requires:	%{qtsensors} = %{EVRD}

%description -n %{qtsensorsd}
Development files for the QtSensors library.

%files -n %{qtsensorsd}
%{_qt5_includedir}/QtSensors
%{_qt5_libdir}/libQt%{api}Sensors.so
%{_qt5_libdir}/libQt%{api}Sensors.prl
%{_qt5_libdir}/cmake/Qt%{api}Sensors
%{_qt5_libdir}/pkgconfig/Qt%{api}Sensors.pc
%{_qt5_prefix}/mkspecs/modules/*.pri
%{_qt5_exampledir}/sensors
%{_qt5_exampledir}/qtsensors

#----------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir
%apply_patches

%build
%qmake_qt5

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}
## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
